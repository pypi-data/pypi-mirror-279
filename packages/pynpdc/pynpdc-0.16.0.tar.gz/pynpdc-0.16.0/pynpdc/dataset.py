from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
import mimetypes
import os
from requests_toolbelt.multipart.encoder import MultipartEncoder  # type: ignore
import requests
import shutil
from typing import (
    Any,
    BinaryIO,
    Dict,
    Generic,
    Iterator,
    Optional,
    Tuple,
    TypeVar,
    cast,
)
from typing_extensions import Self
from urllib.parse import urlencode
import urllib3
from werkzeug.utils import secure_filename

from .auth import AuthContainer
from .exception import APIException, MissingAccountException, MissingClientException
from .types import (
    AttachmentAPIResponse,
    DatasetAPIResponse,
    DatasetContent,
    PermissionAPIResponse,
    UploadInfoAPIResponse,
)

DEFAULT_CHUNK_SIZE = 50

DATASET_STAGING_ENTRYPOINT = "https://beta.data.npolar.no/-/api/"
DATASET_LIFE_ENTRYPOINT = "https://next.api.npolar.no/"


def to_datetime(value: str) -> datetime | None:
    if value.startswith("0001-01-01"):
        return None
    return datetime.fromisoformat(value[:19])


def guard_dir(dir: str) -> None:
    if not os.path.isdir(dir):
        raise FileNotFoundError(f"Path {dir} is not a dir")


def guard_path(path: str) -> None:
    if not os.access(path, os.R_OK):
        raise FileNotFoundError(f"Path {path} not found")
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Path {path} is not a file")


R = TypeVar("R", "AttachmentAPIResponse", "DatasetAPIResponse")
T = TypeVar("T", "Attachment", "Dataset")


class DatasetType(Enum):
    """
    The type of a dataset

    Attributes:
        DRAFT     enum value for a draft dataset. It can be made internal or
                  public in the frontend
        INTERNAL  enum value for an internal dataset
        PUBLIC    enum value for a public dataset
    """

    DRAFT = "draft"
    INTERNAL = "internal"
    PUBLIC = "public"


class Model(Generic[R], ABC):
    """
    A single Model as Dataset or Attachment, that has been retrieved using the
    DatasetClient.

    Attributes:
        client (DatasetClient | None) The client for the dataset module
    """

    client: Optional[DatasetClient]

    created: Optional[datetime]
    created_by: str
    id: str
    modified: Optional[datetime]
    modified_by: str
    permissions: Optional[Permission]

    def __init__(self, raw: R, *, client: Optional[DatasetClient] = None):
        """
        Initialize an instance of a model class as Dataset or Attachment.

        Args:
            raw (R): The API response as parsed JSON
            client (DatasetClient): The used dataset client
        """

        self.client = client

        self.created = to_datetime(raw["created"])
        self.created_by = raw["createdBy"]
        self.id = raw["id"]
        self.modified = to_datetime(raw["modified"])
        self.modified_by = raw["modifiedBy"]
        if "permissions" in raw:
            self.permissions = Permission(raw["permissions"])


class Attachment(Model[AttachmentAPIResponse]):
    """
    The metadata of a single Attachment retrieved from the NPDC dataset module.
    """

    byte_size: int
    dataset_id: str
    description: str
    filename: str
    mime_type: str
    released: Optional[datetime]
    sha256: str
    title: str

    def __init__(
        self, raw: AttachmentAPIResponse, *, client: Optional[DatasetClient] = None
    ) -> None:
        super().__init__(raw, client=client)

        self.byte_size = raw["byteSize"]
        self.dataset_id = raw["datasetId"]
        self.description = raw["description"]
        self.filename = raw["filename"]
        self.mime_type = raw["mimeType"]
        self.released = to_datetime(raw["released"])
        self.sha256 = raw["sha256"]
        self.title = raw["title"]

    def reader(self) -> urllib3.response.HTTPResponse:
        """
        Retrieve a reader to stream the attachment content.

        This is a shortcut for DatasetClient.get_attachment_reader.

        Raises:
            MissingClientException: when no DatasetClient is available

        Returns:
            urllib3.response.HTTPResponse: a response object with read access to
                the body

        """
        if self.client is None:
            raise MissingClientException()
        return self.client.get_attachment_reader(self.dataset_id, self.id)


class Dataset(Model[DatasetAPIResponse]):
    """
    The metadata of a single Dataset retrieved from the NPDC dataset module.

    The user generated metadata as dataset title, geographical information,
    contributors or timeframes are found in the content property.
    """

    content: DatasetContent
    doi: Optional[str]
    published: Optional[datetime]
    published_by: Optional[str] = None
    type: DatasetType

    def __init__(
        self, raw: DatasetAPIResponse, *, client: Optional[DatasetClient] = None
    ) -> None:
        super().__init__(raw, client=client)

        self.content = raw["content"]
        self.doi = raw["doi"]
        self.published = to_datetime(raw["published"])
        self.type = DatasetType(raw["type"])

        published_by = raw["publishedBy"]
        if published_by != "":
            self.published_by = published_by

    def get_attachments(self, **query: Any) -> AttachmentCollection:
        """
        Retrieve attachment metadata filtered by query for the dataset.

        This is a shortcut for DatasetClient.get_attachments.

        Args:
            query (dict): optional query parameters for filtering

        Raises:
            MissingClientException: when no DatasetClient is available

        Returns:
            AttachmentCollection: a lazy collection of attachments
        """
        if self.client is None:
            raise MissingClientException()
        return self.client.get_attachments(self.id, **query)

    def download_attachments_as_zip(self, target_dir: str) -> str:
        """
        Download all dataset attachments as a zip file.

        This is a shortcut for DatasetClient.download_attachments_as_zip.

        Args:
            target_dir (str): the target directory where the ZIP file should be
                saved.

        Raises:
            MissingClientException: when no DatasetClient is available

        Returns:
            str: The path of the downloaded ZIP file
        """
        if self.client is None:
            raise MissingClientException()
        return self.client.download_attachments_as_zip(self.id, target_dir)


class Permission:
    object_id: str
    user_id: Optional[str]
    may_read: bool
    may_update: bool
    may_delete: bool

    def __init__(self, raw: PermissionAPIResponse):
        """
        Initialize an instance of a Permission.

        Args:
            raw (PermissionAPIResponse): The API response as parsed JSON
        """

        self.object_id = raw["objectId"]
        self.user_id = raw.get("userId")
        self.may_read = raw["mayRead"]
        self.may_update = raw["mayUpdate"]
        self.may_delete = raw["mayDelete"]


class LazyCollection(Generic[T], ABC):
    chunk_size: int
    client: DatasetClient
    model_class: type[Attachment | Dataset]
    query: dict[str, Any]
    skip: int
    take: int | None
    _generator: Iterator[T]

    def __init__(
        self,
        *,
        client: DatasetClient,
        chunk_size: int = DEFAULT_CHUNK_SIZE,
        **query: Any,
    ) -> None:
        if chunk_size < 1 or chunk_size > 255:
            raise ValueError("Chunk size have to be between 1 and 255")

        self.client = client
        self.chunk_size = chunk_size
        self.skip = query.get("skip", 0)
        self.take = query.get("take")  # if not set, take all datasets
        self.query = query

        self._generator = self._generate()

    @property
    @abstractmethod
    def _endpoint(self) -> str:
        pass

    def _request(self, query: Dict[str, Any]) -> requests.Response:
        url = self._endpoint + "?" + urlencode(query)
        return self.client._exec_request("GET", url)

    def _generate(self) -> Iterator[T]:
        chunk_size = self.chunk_size
        if self.take is not None and self.take < chunk_size:
            chunk_size = self.take

        query = {
            **self.query,
            "take": chunk_size,
            "skip": self.skip,
        }

        c = 0
        while True:
            resp = self._request(query)
            raw = resp.json()

            items = raw["items"]
            for data in items:
                yield cast(T, self.model_class(data, client=self.client))
                c += 1
                if self.take is not None and c >= self.take:
                    return  # data complete

            query["skip"] += query["take"]

            if len(items) < chunk_size:
                break  # no more chunks

    def __iter__(self) -> Self:
        return self

    def __next__(self) -> T:
        return next(self._generator)


class AttachmentCollection(LazyCollection[Attachment]):
    """
    A generator to retrieve Attachment models in a lazy way.

    LazyCollection will retrieve models in chunks and yield each model until
    all models for the query have been received.

    Attributes:
        dataset_id (str): the ID of the dataset the attachment is related to
        client (DatasetClient): the client used to request models
        chunk_size (int): the number of models fetched per chunk size
        skip (int): the number of models to skip
        take (int): the number of models to retrieve
        query (dict): additional query parameters. Check the API documentation
            for details:
            https://beta.data.npolar.no/-/docs/dataset/#/attachment/get_dataset__datasetId__attachment_
    """

    model_class = Attachment

    def __init__(
        self, dataset_id: str, *, client: DatasetClient, **kwargs: Any
    ) -> None:
        super().__init__(client=client, **kwargs)
        self.dataset_id = dataset_id

    @property
    def _endpoint(self) -> str:
        return f"{self.client.entrypoint}dataset/{self.dataset_id}/attachment/"


class DatasetCollection(LazyCollection[Dataset]):
    """
    A generator to retrieve Dataset models in a lazy way.

    LazyCollection will retrieve models in chunks and yield each model until
    all models for the query have been received.

    Attributes:
        client (DatasetClient): the client used to request models
        chunk_size (int): the number of models fetched per chunk size
        skip (int): the number of models to skip
        take (int): the number of models to retrieve
        query (dict): additional query parameters. Check the API documentation
            for details:
            https://beta.data.npolar.no/-/docs/dataset/#/dataset/get_dataset_
    """

    model_class = Dataset

    def __init__(self, *, client: DatasetClient, **kwargs: Any) -> None:
        type_arg = kwargs.get("type")
        if type(type_arg) is DatasetType:
            kwargs["type"] = type_arg.value

        super().__init__(client=client, **kwargs)

    @property
    def _endpoint(self) -> str:
        return f"{self.client.entrypoint}dataset/"


class PermissionCollection:
    def __init__(self, raw_permission_list: list[PermissionAPIResponse]) -> None:
        self._generator = iter(raw_permission_list)

    def __iter__(self) -> Self:
        return self

    def __next__(self) -> Permission:
        return Permission(next(self._generator))


class Upload:
    description: str | None
    filename: str
    mime_type: str
    reader: BinaryIO
    title: str | None

    """
    A file upload containing a reader to retrieve the content as well as
    metadata.

    Attributes:
        reader (BinaryIO): a reader
        filename (str): the file name
        description (str | None): an optional description
        title (str | None): an optional title
        mime_type (str) the mime type (a.k.a. content type) of the file
    """

    def __init__(
        self,
        reader: BinaryIO,
        filename: str,
        description: Optional[str] = None,
        title: Optional[str] = None,
        mime_type: Optional[str] = None,
    ) -> None:
        """
        Initialize an Upload instance

        Args:
            reader (BinaryIO): reader to fetch the data
            filename (str): the file name
            description (str | None): an optional description
            title (str | None): an optional title
            mime_type (str):
                the mime type (a.k.a. content type) of the file. When None it
                will be set to ""application/octet-stream"
        """

        self.reader = reader
        self.filename = filename
        self.description = description
        self.title = title
        if mime_type is None:
            self.mime_type = "application/octet-stream"
        else:
            self.mime_type = mime_type

    def _get_multiparts(self) -> list[Tuple[Any, ...]]:
        data: list[Tuple[Any, ...]] = []

        if self.description is not None:
            data.append(
                ("description", self.description),
            )
        if self.title is not None:
            data.append(
                ("title", self.title),
            )
        # blob has to be the last tuple to add to the list
        data.append(
            ("blob", (self.filename, self.reader, self.mime_type)),
        )

        return data


class UploadInfo:
    """
    Information of an uploaded attachment
    """

    id: str
    filename: str
    sha256: str

    def __init__(self, raw: UploadInfoAPIResponse) -> None:
        self.id = raw["id"]
        self.filename = raw["fileName"]
        self.sha256 = raw["sha256"]


class DatasetClient:
    entrypoint: str
    auth: Optional[AuthContainer]
    verify_ssl: bool

    """
    A client to communicate with the NPDC dataset module

    Attributes:
        entrypoint (str): The entrypoint of the Rest API with a trailing slash
        verify_ssl (bool): Set to false, when the Rest API has a self signed
            certificate
        token (str | None): A login token as returned from AuthClient.login.
            This is needed for accessing non-public data or changing data.
    """

    def __init__(
        self,
        entrypoint: str,
        *,
        verify_ssl: bool = True,
        auth: Optional[AuthContainer] = None,
    ) -> None:
        """
        Create a new DatasetClient.

        Args:
            entrypoint (str): The entrypoint of the Rest API with a trailing
                slash
            verify_ssl (bool): Set to false, when the Rest API has a self signed
                certificate
            auth (AuthContainer): An optional Account object used for
                authentification.
        """
        self.entrypoint = entrypoint
        self.auth = auth
        self.verify_ssl = verify_ssl

    def _exec_request(
        self, method: str, endpoint: str, *, data: Any = None, stream: bool = False
    ) -> requests.Response:
        if method != "GET" and self.auth is None:
            raise MissingAccountException

        kwargs: dict[str, Any] = {"verify": self.verify_ssl, "stream": stream}

        if self.auth is not None:
            kwargs["headers"] = self.auth.headers

        if type(data) is MultipartEncoder:
            kwargs["headers"]["Content-Type"] = data.content_type
            kwargs["data"] = data
        elif type(data) is dict:
            kwargs["json"] = data
        elif data is not None:
            raise ValueError("Unknown data format")

        response = requests.request(method, endpoint, **kwargs)

        if response.status_code > 201:
            raise APIException(response)

        return response

    def create_dataset(self, content: DatasetContent) -> Dataset:
        """
        Save a new dataset in the NPDC dataset module.

        Args:
            content (DatasetContent): The user generated dataset content.

        Returns:
            Dataset: the created dataset including the ID and file metadata

        Raises:
            ValueError: if the content arg is not a dict
            APIException: If HTTP status code > 201. Mostly this will be an
                authentification or authorisation issue.

        """
        if not isinstance(content, dict):
            raise ValueError("content has to be a dict")

        endpoint = f"{self.entrypoint}dataset/"
        response = self._exec_request("POST", endpoint, data=content)
        return Dataset(response.json(), client=self)

    def get_datasets(
        self, chunk_size: int = DEFAULT_CHUNK_SIZE, **query: Any
    ) -> DatasetCollection:
        """
        Retrieve a list of datasets by query.

        The return value is a DatasetCollection that yields the Datasets when
        used in a for loop.

        Example:
            client = DatasetClient(DATASET_LIFE_ENTRYPOINT)
            query = "fimbulisen"
            for dataset in client.get_datasets(q=query):
                print(dataset.id, dataset.content["title"])

        Args:
            chunk_size (int): the number of models fetched per chunk size
            query (dict):
                the query for the dataset retreival. See
                https://beta.data.npolar.no/-/docs/dataset/#/dataset/get_dataset_
                for details

        Returns:
            DatasetCollection an iterator to fetch the Dataset objects
        """
        return DatasetCollection(client=self, **query, chunk_size=chunk_size)

    def get_dataset(self, dataset_id: str) -> Dataset | None:
        """
        Retrieve a single dataset by ID.

        When the dataset is not found, None is returned.

        Args:
            dataset_id (str): the UUID of the dataset

        Returns:
            Dataset | None

        Raises:
            APIException: If HTTP status code is neither 200 or 404. Mostly this
                will be an authentification or authorisation issue.
        """
        endpoint = f"{self.entrypoint}dataset/{dataset_id}"

        try:
            response = self._exec_request("GET", endpoint)
        except APIException as e:
            if e.status_code == 404:
                return None
            raise e

        return Dataset(response.json(), client=self)

    def update_dataset(self, dataset_id: str, content: DatasetContent) -> Dataset:
        """
        Update the metadata of a dataset.

        Args:
            dataset_id (str): the UUID of the dataset
            content (DatasetContent): The user generated dataset content.

        Returns:
            Dataset: the updated dataset

        Raises:
            ValueError: if the content arg is not a dict
            APIException: If HTTP status code > 201. Mostly this will be an
                authentification or authorisation issue.
        """
        if not isinstance(content, dict):
            raise ValueError("content has to be a dict")

        endpoint = f"{self.entrypoint}dataset/{dataset_id}"
        response = self._exec_request("PUT", endpoint, data=content)
        return Dataset(response.json(), client=self)

    def delete_dataset(self, dataset_id: str) -> None:
        """
        Delete the dataset.

        Args:
            dataset_id (str): the UUID of the dataset

        Raises:
            APIException: If HTTP status code > 201. Mostly this will be an
                authentification or authorisation issue.
        """
        endpoint = f"{self.entrypoint}dataset/{dataset_id}"
        self._exec_request("DELETE", endpoint)

    def get_attachments(
        self, dataset_id: str, chunk_size: int = DEFAULT_CHUNK_SIZE, **query: Any
    ) -> AttachmentCollection:
        """
        Retrieve a list of attachments by query

        The return value is an AttachmentCollection that yields the Datasets
        when used in a for loop.

        Args:
            dataset_id (str): the UUID of the related dataset
            chunk_size (int): the number of models fetched per chunk size
            query (dict):
                the query for the attachment retreival. See
                https://beta.data.npolar.no/-/docs/dataset/#/attachment/get_dataset__datasetId__attachment_
                for details

        Returns:
            AttachmentCollection  an iterator to fetch the Attachment objects
        """
        return AttachmentCollection(
            dataset_id, client=self, **query, chunk_size=chunk_size
        )

    def get_attachment(self, dataset_id: str, attachment_id: str) -> Attachment | None:
        """
        Retrieve a single attachment by dataset and attachment ID.

        When the attachment is not found, None is returned.

        Args:
            dataset_id (str): the UUID of the dataset
            attachment_id (str): the UUID of the attachment

        Returns:
            Attachment | None

        Raises:
            APIException: If HTTP status code is neither 200 or 404. Mostly this
                will be an authentification or authorisation issue.
        """
        endpoint = f"{self.entrypoint}dataset/{dataset_id}/attachment/{attachment_id}"

        try:
            response = self._exec_request("GET", endpoint)
        except APIException as e:
            if e.status_code == 404:
                return None
            raise e

        return Attachment(response.json(), client=self)

    def get_attachment_reader(
        self, dataset_id: str, attachment_id: str
    ) -> urllib3.response.HTTPResponse:
        """
        Retrieve a reader to stream the attachment content.

        When the attachment should be downloaded it is simpler to use the method
        download_attachment or download_attachments.

        Args:
            dataset_id (str): The dataset id in form of a UUID
            attachment_id (str): The attachment id in form of a UUID

        Returns:
            stream: A reader to access the attachment content
        """
        endpoint = (
            f"{self.entrypoint}dataset/{dataset_id}/attachment/{attachment_id}/_blob"
        )

        resp = self._exec_request("GET", endpoint, stream=True)
        resp.raw.decode_content = True
        return cast(urllib3.response.HTTPResponse, resp.raw)

    def create_file_upload(self, path: str) -> Upload:
        """
        Create and return an Upload instance that represents a file upload
        including a reader to fetch the data and meta data as filename and
        mime type

        Args:
            path (str): The path of the file to upload. Best practice is to use
                an absolute path

        Returns:
            Upload: An Upload instance

        """
        return Upload(
            open(path, "rb"),
            os.path.basename(path),
            mime_type=mimetypes.guess_type(path)[0],
        )

    def add_attachment(self, dataset_id: str, upload: Upload) -> UploadInfo:
        """
        Add a single attachments to a dataset

        Args:
            dataset_id (str): The dataset id in form of a UUID
            upload: (Upload) An Upload instance

        Returns:
            UploadInfo

        Raises:
            MissingAccountException: If no account is available
            APIException: If HTTP status code > 201. Mostly this will be an
                authentification or authorisation issue.
        """
        return self.add_attachments(dataset_id, [upload])[0]

    def add_attachments(
        self, dataset_id: str, uploads: list[Upload]
    ) -> list[UploadInfo]:
        """
        Add several attachments to a dataset

        Args:
            dataset_id (str): The dataset id in form of a UUID
            uploads: (Upload[]) A list of Upload instances

        Returns:
            UploadInfo[]

        Raises:
            MissingAccountException: If no account is available
            APIException: If HTTP status code > 201. Mostly this will be an
                authentification or authorisation issue.
        """
        endpoint = f"{self.entrypoint}dataset/{dataset_id}/attachment/"
        data: list[Tuple[Any, ...]] = []
        for upload in uploads:
            data = [*data, *upload._get_multiparts()]
        multipart = MultipartEncoder(data)

        response = self._exec_request("POST", endpoint, data=multipart, stream=True)

        return [UploadInfo(item) for item in response.json()]

    def update_attachment(
        self,
        dataset_id: str,
        attachment_id: str,
        *,
        description: str,
        filename: str,
        title: str,
    ) -> Attachment:
        """
        Update the attachment metadata

        Args:
            dataset_id (str): The dataset id in form of a UUID
            attachment_id (str): The attachment id in form of a UUID
            description (str): the description
            filename (str): the file name
            title (str): the title

        Returns:
            Attachment: The updated Attachment metadata

        Raises:
            APIException: If HTTP status code > 201. Mostly this will be an
                authentification or authorisation issue.
        """
        endpoint = f"{self.entrypoint}dataset/{dataset_id}/attachment/{attachment_id}"
        payload = {"description": description, "filename": filename, "title": title}

        response = self._exec_request("PUT", endpoint, data=payload)
        return Attachment(response.json(), client=self)

    def delete_attachment(self, dataset_id: str, attachment_id: str) -> None:
        """
        Delete the attachment.

        Args:
            dataset_id (str): the UUID of the dataset
            attachment_id (str): the UUID of the attachment

        Raises:
            APIException: If HTTP status code > 201. Mostly this will be an
                authentification or authorisation issue.
        """
        endpoint = f"{self.entrypoint}dataset/{dataset_id}/attachment/{attachment_id}"
        self._exec_request("DELETE", endpoint)

    def download_attachments_as_zip(self, dataset_id: str, target_dir: str) -> str:
        """
        Download all dataset attachments as a zip file.

        Args:
            dataset_id (str): the UUID of the dataset
            target_dir (str): the directory the zip file is downloaded to

        Returns:
            str: the path of the zip file

        Raises:
            FileNotFoundError: target_dir is not a directory
            APIException: If HTTP status code > 201. Mostly this will be an
                authentification or authorisation issue.
        """
        guard_dir(target_dir)

        endpoint = f"{self.entrypoint}dataset/{dataset_id}/attachment/_blob"
        resp = self._exec_request("GET", endpoint, stream=True)
        resp.raw.decode_content = True

        filename = f"{dataset_id}_files.zip"
        path = os.path.join(target_dir, filename)
        with resp.raw as src:
            with open(path, "wb") as dest:
                shutil.copyfileobj(src, dest)

        return path

    def download_attachment(
        self, dataset_id: str, attachment_id: str, target_dir: str
    ) -> str | None:
        """
        Download an attachment of a dataset.

        For security reasons the filename of the downloaded file may differ
        from the filename in the attachment metadata

        Args:
            dataset_id (str): the UUID of the dataset
            attachment_id (str): the UUID of the attachment
            target_dir (str): the directory the attachments is downloaded to

        Returns:
            str: the path of the file

        Raises:
            FileNotFoundError: target_dir is not a directory
            APIException: If HTTP status code > 201. Mostly this will be an
                authentification or authorisation issue.
        """
        guard_dir(target_dir)

        attachment = self.get_attachment(dataset_id, attachment_id)
        if attachment is None:
            return None

        filename = secure_filename(attachment.filename)

        path = os.path.join(target_dir, filename)
        with attachment.reader() as src:
            with open(path, "wb") as dest:
                shutil.copyfileobj(src, dest)

        return path

    def upload_attachments(self, dataset_id: str, paths: list[str]) -> list[UploadInfo]:
        """
        Upload a number of attachments to the dataset

        It is not possible to provide title and description. If this is crucial
        use upload_attachment

        Args:
            dataset_id (str): the UUID of the dataset
            paths (str[]): a list of paths of the files to upload. Best practice
                is to use absolute paths

        Returns:
            UploadInfo[]

        Raises:
            FileNotFoundError: one or more paths do not exist
            MissingAccountException: If no account is available
            APIException: If HTTP status code > 201. Mostly this will be an
                authentification or authorisation issue.
        """
        map(guard_path, paths)

        uploads = [self.create_file_upload(path) for path in paths]
        return self.add_attachments(dataset_id, uploads)

    def upload_attachment(
        self,
        dataset_id: str,
        path: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
    ) -> UploadInfo:
        """
        Upload a number of attachments to the dataset

        Args:
            dataset_id (str): the UUID of the dataset
            path (str): the path of the file to upload. Best practice is to use
                an absolute path
            title (str | None): an optional title
            description (str | None): an optional description

        Returns:
            UploadInfo

        Raises:
            FileNotFoundError: one or more paths do not exist
            MissingAccountException: If no account is available
            APIException: If HTTP status code > 201. Mostly this will be an
                authentification or authorisation issue.
        """
        guard_path(path)

        upload = self.create_file_upload(path)
        upload.title = title
        upload.description = description

        return self.add_attachment(dataset_id, upload)

    def add_permission(
        self,
        dataset_id: str,
        user_id: str,
        *,
        may_read: bool = False,
        may_update: bool = False,
        may_delete: bool = False,
    ) -> Permission:
        """
        Add user permissions to a dataset

        Args:
            dataset_id (str): the UUID of the dataset
            user_id (str): the UUID of the user account
            may_read (bool): the read permission for this dataset
            may_update (bool): the update permission for this dataset
            may_delete (bool): the delete permission for this dataset

        Returns:
            Permission

        Raises:
            APIException: If HTTP status code > 201. Mostly this will be an
                authentification or authorisation issue.
        """
        raw = {
            "userId": user_id,
            "mayRead": may_read,
            "mayUpdate": may_update,
            "mayDelete": may_delete,
        }
        endpoint = f"{self.entrypoint}dataset/{dataset_id}/permission/"
        response = self._exec_request("POST", endpoint, data=raw)
        perm_response: PermissionAPIResponse = response.json()
        return Permission(perm_response)

    def get_permissions(self, dataset_id: str) -> PermissionCollection:
        """
        Retrieve a list of permissions of a dataset

        The return value is an PermissionCollection that yields the Permissions
        when used in a for loop.

        Args:
            dataset_id (str): the UUID of the dataset

        Returns:
            PermissionCollection an iterator to fetch the Permission objects
        """
        endpoint = f"{self.entrypoint}dataset/{dataset_id}/permission/"
        response = self._exec_request("GET", endpoint)
        raw = response.json()
        return PermissionCollection(raw["items"])

    def get_permission(self, dataset_id: str, user_id: str) -> Permission | None:
        """
        Get user permissions of a dataset

        Args:
            dataset_id (str): the UUID of the dataset
            user_id (str): the UUID of the user account

        Returns:
            Permission

        Raises:
            APIException: If HTTP status code is neither 200 or 404. Mostly this
                will be an authentification or authorisation issue.

        """
        endpoint = f"{self.entrypoint}dataset/{dataset_id}/permission/{user_id}"

        try:
            response = self._exec_request("GET", endpoint)
        except APIException as e:
            if e.status_code == 404:
                return None
            raise e

        raw = response.json()
        return Permission(raw)

    def update_permission(
        self,
        dataset_id: str,
        user_id: str,
        *,
        may_read: bool = False,
        may_update: bool = False,
        may_delete: bool = False,
    ) -> Permission:
        """
        Update user permissions of a dataset

        Args:
            dataset_id (str): the UUID of the dataset
            user_id (str): the UUID of the user account
            may_read (bool): the read permission for this dataset
            may_update (bool): the update permission for this dataset
            may_delete (bool): the delete permission for this dataset

        Returns:
            Permission

        Raises:
            APIException: If HTTP status code > 201. Mostly this will be an
                authentification or authorisation issue.
        """
        raw = {
            "mayRead": may_read,
            "mayUpdate": may_update,
            "mayDelete": may_delete,
        }
        endpoint = f"{self.entrypoint}dataset/{dataset_id}/permission/{user_id}"
        response = self._exec_request("PUT", endpoint, data=raw)
        perm_response: PermissionAPIResponse = response.json()
        return Permission(perm_response)

    def delete_permission(self, dataset_id: str, user_id: str) -> None:
        """
        Delete user permissions of a dataset

        Args:
            dataset_id (str): the UUID of the dataset
            user_id (str): the UUID of the user account
        """
        endpoint = f"{self.entrypoint}dataset/{dataset_id}/permission/{user_id}"
        self._exec_request("DELETE", endpoint)
