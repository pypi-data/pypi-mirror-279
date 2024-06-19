from datetime import datetime
import hashlib
import io
import os
import pytest
import shutil
import tempfile
import unittest
from urllib.parse import urlencode
import urllib3
import uuid
import zipfile

from pynpdc.auth import AuthClient
from pynpdc.dataset import (
    DEFAULT_CHUNK_SIZE,
    Attachment,
    AttachmentCollection,
    Dataset,
    DatasetClient,
    DatasetCollection,
    Permission,
    PermissionCollection,
    DatasetType,
    Upload,
    UploadInfo,
    guard_dir,
    guard_path,
)
from pynpdc.exception import (
    APIException,
    MissingAccountException,
    MissingClientException,
)

from .helpers import create_invalid_test_auth, get_test_config

"""
Prerequisites for this test suite:

- a user foo@example.org with password 1234123412341234 has to exist in auth
- another user data@npolar.no with ID 0407a671-4b6b-4dc8-b4aa-49a08bf56f96 has
  to exist in auth
- at least one public dataset with id PUBLIC_ID has to exist
- the public dataset must have one file, that is not too large to avoid
  performance issues in the test
"""


class TestGuardDir(unittest.TestCase):
    def test_with_dir(self):
        path = os.path.dirname(__file__)
        guard_dir(path)
        self.assertTrue(True)

    def test_with_file(self):
        path = __file__
        with pytest.raises(FileNotFoundError):
            guard_dir(path)

    def test_with_unknown_path(self):
        path = f"/tmp/{ uuid.uuid4() }"
        with pytest.raises(FileNotFoundError):
            guard_dir(path)


class TestGuardPath(unittest.TestCase):
    def test_with_dir(self):
        path = os.path.dirname(__file__)
        with pytest.raises(FileNotFoundError):
            guard_path(path)

    def test_with_file(self):
        path = __file__
        guard_path(path)
        self.assertTrue(True)

    def test_with_unknown_path(self):
        path = f"/tmp/{ uuid.uuid4() }"
        with pytest.raises(FileNotFoundError):
            guard_path(path)


@pytest.fixture(scope="class")
def run_fixtures(request):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    # config
    cfg = get_test_config()

    # anonymous_client
    request.cls.anonymous_client = DatasetClient(
        cfg["kinko"]["entrypoint"], verify_ssl=False
    )

    # authorized_client
    auth_client = AuthClient(cfg["komainu"]["entrypoint"], verify_ssl=False)
    account = auth_client.login(
        cfg["komainu"]["testUser"], cfg["komainu"]["testPassword"]
    )
    request.cls.authorized_client = DatasetClient(
        cfg["kinko"]["entrypoint"], auth=account, verify_ssl=False
    )
    request.cls.authorized_user_id = account.id

    # client with invalid token
    auth = create_invalid_test_auth()
    request.cls.invalid_token_client = DatasetClient(
        cfg["kinko"]["entrypoint"], auth=auth, verify_ssl=False
    )

    # tag
    request.cls.tag = cfg["kinko"]["summaryTag"]

    # cleanup of previous run
    for dataset in request.cls.authorized_client.get_datasets(q=request.cls.tag):
        if dataset.type == DatasetType.DRAFT:
            request.cls.authorized_client.delete_dataset(dataset.id)

    # draft dataset
    content = {
        "title": "unittest draft dataset #pynpdcdraft",
        "summary": request.cls.tag,
    }
    dataset = request.cls.authorized_client.create_dataset(content)
    request.cls.DRAFT_ID = dataset.id

    # public dataset
    request.cls.PUBLIC_ID = cfg["kinko"]["publicID"]

    # other user (for Account tests)
    request.cls.OTHER_USER_ID = cfg["komainu"]["otherUserID"]


@pytest.mark.usefixtures("run_fixtures")
class TestDataset(unittest.TestCase):
    def setUp(self):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    # FIXTURES

    def _create_draft(self, title="Draft dataset"):
        content = dict(title=f"[pynpdc unit test] {title}", summary=self.tag)
        dataset = self.authorized_client.create_dataset(content)
        self.assertIsInstance(dataset, Dataset)
        return dataset.id

    # READ DATASET COLLECTION

    def test_get_datasets(self):
        title = "pynpdcmasscreate"
        total_num = 5
        for i in range(total_num):
            self._create_draft(f"{title} {i}")

        tests = [
            # query, num returned items, chunk_size of lazy collection
            (dict(q=title), 5, DEFAULT_CHUNK_SIZE),
            (dict(q=title), 5, 5),
            (dict(q=title), 5, 2),
            (dict(q=title), 5, 1),
            (dict(q=title, skip=3), 2, DEFAULT_CHUNK_SIZE),
            (dict(q=title, take=1), 1, DEFAULT_CHUNK_SIZE),
            (dict(q=title, take=4), 4, 3),
            (dict(q=title, skip=1, take=2), 2, 1),
        ]

        for query, item_num, chunk_size in tests:
            msg = urlencode(query)

            gen = self.authorized_client.get_datasets(**query, chunk_size=chunk_size)
            self.assertIsInstance(gen, DatasetCollection, msg)

            datasets = list(gen)
            self.assertGreaterEqual(len(datasets), item_num, msg)

        if item_num > 0:
            # check 1st item
            self.assertIsInstance(datasets[0], Dataset, msg)
            self.assertEqual(datasets[0].type, DatasetType.DRAFT, msg)

    def test_get_only_draft_datasets(self):
        self._create_draft("draftexample")

        datasets = list(self.authorized_client.get_datasets(type=DatasetType.DRAFT))
        self.assertGreater(len(datasets), 0)

        for dataset in datasets:
            self.assertEqual(dataset.type, DatasetType.DRAFT)

    def test_get_datasets_by_iterator(self):
        self._create_draft("pynpdciterator 1")
        self._create_draft("pynpdciterator 2")

        gen = self.authorized_client.get_datasets(q="pynpdciterator")

        dataset = next(gen)
        self.assertIsInstance(dataset, Dataset)
        dataset = next(gen)
        self.assertIsInstance(dataset, Dataset)

    def test_getting_datasets_with_invalid_chunk_size_fails(self):
        with pytest.raises(ValueError):
            self.anonymous_client.get_datasets(chunk_size=0)

        with pytest.raises(ValueError):
            self.anonymous_client.get_datasets(chunk_size=1000)

    # READ DATASET

    def test_read_single_public_dataset(self):
        dataset = self.anonymous_client.get_dataset(self.PUBLIC_ID)

        self.assertIsInstance(dataset, Dataset)
        self.assertEqual(dataset.id, self.PUBLIC_ID)
        self.assertEqual(dataset.type, DatasetType.PUBLIC)
        self.assertIsInstance(dataset.published, datetime)
        self.assertIsInstance(dataset.published_by, str)
        self.assertIsInstance(dataset.permissions, Permission)
        self.assertIsInstance(dataset.permissions.may_read, bool)
        self.assertTrue(dataset.permissions.may_read)

    def test_reading_draft_dataset_without_auth_fails(self):
        dataset = self.anonymous_client.get_dataset(self.DRAFT_ID)

        self.assertIsNone(dataset)

    def test_reading_draft_dataset_with_auth(self):
        dataset = self.authorized_client.get_dataset(self.DRAFT_ID)

        self.assertIsInstance(dataset, Dataset)
        self.assertEqual(dataset.id, self.DRAFT_ID)
        self.assertEqual(dataset.type, DatasetType.DRAFT)
        self.assertIsNone(dataset.published)
        self.assertIsNone(dataset.published_by)

    def test_reading_non_existent_dataset_fails(self):
        dataset_id = uuid.uuid4()

        dataset = self.anonymous_client.get_dataset(dataset_id)

        self.assertIsNone(dataset)

    def test_reading_datadet_with_invalid_token_fails(self):
        dataset_id = uuid.uuid4()

        with pytest.raises(APIException):
            self.invalid_token_client.get_dataset(dataset_id)

    # CREATE DATASET

    def test_create_dataset(self):
        content = dict(
            title="Draft dataset created by pynpdc unit test", summary=self.tag
        )

        dataset = self.authorized_client.create_dataset(content)

        self.assertIsInstance(dataset, Dataset)
        self.assertDictEqual(dataset.content, content)
        self.assertTrue(dataset.doi.startswith("10.21334/"))
        self.assertIsInstance(dataset.created, datetime)
        self.assertIsInstance(dataset.modified, datetime)
        self.assertEqual(dataset.created_by, self.authorized_user_id)
        self.assertEqual(dataset.modified_by, self.authorized_user_id)
        self.assertIsNone(dataset.published)
        self.assertIsNone(dataset.published_by)

        dataset = self.authorized_client.get_dataset(dataset.id)
        self.assertDictEqual(dataset.content, content)

    def test_creating_dataset_without_auth_fails(self):
        content = dict(title="Dataset created by pynpdc unit test")

        with pytest.raises(MissingAccountException):
            self.anonymous_client.create_dataset(content)

    def test_creating_dataset_with_wrong_class_fails(self):
        content = "a string"

        with pytest.raises(ValueError):
            self.authorized_client.create_dataset(content)

    # UPDATE DATASET

    def test_update_dataset(self):
        content = dict(
            title="Draft dataset for updating created by pynpdc unit test",
            summary=self.tag,
        )

        dataset = self.authorized_client.create_dataset(content)
        self.assertIsInstance(dataset, Dataset)

        new_content = dict(
            title="Updated draft dataset created by pynpdc unit test", summary=self.tag
        )

        self.authorized_client.update_dataset(dataset.id, new_content)

        dataset = self.authorized_client.get_dataset(dataset.id)
        self.assertDictEqual(dataset.content, new_content)

    def test_updating_dataset_with_wrong_class_fails(self):
        content = dict(
            title="Draft dataset for updating created by pynpdc unit test",
            summary=self.tag,
        )

        dataset = self.authorized_client.create_dataset(content)
        self.assertIsInstance(dataset, Dataset)

        with pytest.raises(ValueError):
            self.authorized_client.update_dataset(dataset.id, "a string")

    # DELETE DATASET

    def test_delete_dataset(self):
        content = dict(
            title="Dataset for deletion created by pynpdc unit test", summary=self.tag
        )

        dataset = self.authorized_client.create_dataset(content)
        id = dataset.id

        dataset = self.authorized_client.get_dataset(id)
        self.assertEqual(dataset.id, id)

        self.authorized_client.delete_dataset(id)

        dataset = self.authorized_client.get_dataset(id)
        self.assertIsNone(dataset)

    def test_deleting_public_dataset_fails(self):
        with pytest.raises(APIException) as e_info:
            self.authorized_client.delete_dataset(self.PUBLIC_ID)
        self.assertEqual(e_info.value.status_code, 403)

    # OTHER TESTS

    def test_exec_request_with_unknown_data_type(self):
        with pytest.raises(ValueError):
            self.authorized_client._exec_request("POST", "/whatever/", data=3)


@pytest.mark.usefixtures("run_fixtures")
class TestAttachment(unittest.TestCase):
    def setUp(self):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    # FIXTURES

    def _create_draft(self):
        content = dict(
            title="Draft dataset created by pynpdc unit test", summary=self.tag
        )
        dataset = self.authorized_client.create_dataset(content)
        self.assertIsInstance(dataset, Dataset)
        return dataset.id

    def _create_attachment(
        self, dataset_id, content, filename="test.txt", *, mime_type="text/plain"
    ):
        upload = Upload(io.BytesIO(content), filename, mime_type=mime_type)
        info = self.authorized_client.add_attachment(dataset_id, upload)
        return info.id

    @property
    def _file_tests(self):
        return {
            "upload-download-1.txt": b"File content 1",
            "upload-download-2.json": b'{"content": "File content 2"}',
            "upload-download-3.tsv": b"Name\tIndex\nFile content 3\t3",
        }

    # READ ATTACHMENT COLLECTION

    def test_read_attachments_through_client(self):
        gen = self.anonymous_client.get_attachments(self.PUBLIC_ID, take=1)
        self.assertIsInstance(gen, AttachmentCollection)

        attachments = list(gen)
        self.assertEqual(len(attachments), 1)
        self.assertIsInstance(attachments[0], Attachment)
        self.assertIsInstance(attachments[0].permissions, Permission)

    def test_read_attachments_through_dataset(self):
        dataset = self.anonymous_client.get_dataset(self.PUBLIC_ID)
        self.assertIsNotNone(dataset)

        gen = dataset.get_attachments(take=1)
        self.assertIsInstance(gen, AttachmentCollection)

        attachments = list(gen)
        self.assertEqual(len(attachments), 1)
        self.assertIsInstance(attachments[0], Attachment)

    # READ ATTACHMENT METADATA

    def test_read_single_attachment(self):
        gen = self.anonymous_client.get_attachments(self.PUBLIC_ID, take=1)
        attachments = list(gen)
        self.assertEqual(len(attachments), 1)
        attachment_id = attachments[0].id

        attachment = self.anonymous_client.get_attachment(self.PUBLIC_ID, attachment_id)

        self.assertIsInstance(attachment, Attachment)
        self.assertEqual(attachment_id, attachment.id)
        self.assertIsInstance(attachment.permissions, Permission)

    def test_reading_non_existent_attachment_fails(self):
        attachment_id = uuid.uuid4()

        attachment = self.anonymous_client.get_attachment(self.PUBLIC_ID, attachment_id)

        self.assertIsNone(attachment)

    def test_reading_attachment_with_invalid_token_fails(self):
        dataset_id = uuid.uuid4()
        attachment_id = uuid.uuid4()

        with pytest.raises(APIException):
            self.invalid_token_client.get_attachment(dataset_id, attachment_id)

    # READ ATTACHMENT CONTENT

    def test_read_attachment_content(self):
        gen = self.anonymous_client.get_attachments(self.PUBLIC_ID, take=1)
        attachments = list(gen)
        self.assertEqual(len(attachments), 1)
        attachment = attachments[0]

        m = hashlib.sha256()
        with attachment.reader() as src:
            for chunk in src:
                m.update(chunk)

        sha = m.hexdigest()
        self.assertEqual(attachment.sha256, sha)

    def test_write_attachment_content_to_file(self):
        """This test is more thought as a use case for documentation than a
        necessary unit test"""

        gen = self.anonymous_client.get_attachments(self.PUBLIC_ID, take=1)
        attachments = list(gen)

        self.assertEqual(len(attachments), 1)
        attachment = attachments[0]

        # part 1: stream content to bytes

        b = io.BytesIO()
        with attachment.reader() as src:
            for chunk in src:
                b.write(chunk)
        local_content = b.getvalue()

        # part 2: write to temp file

        with tempfile.TemporaryFile() as dest:
            with attachment.reader() as src:
                shutil.copyfileobj(src, dest)

            dest.seek(0)
            file_content = dest.read()

        self.assertEqual(local_content, file_content)

    # ADD ATTACHMENT

    def test_create_file_upload(self):
        base_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

        tests = [
            (["pynpdc", "exception.py"], "exception.py", "text/x-python"),
            (["Makefile"], "Makefile", "application/octet-stream"),
        ]

        for pp, filename, mime_type in tests:
            path = os.path.join(base_path, *pp)

            upload = self.anonymous_client.create_file_upload(path)
            self.assertIsInstance(upload, Upload)
            self.assertEqual(upload.filename, filename)
            self.assertEqual(upload.mime_type, mime_type)
            # check reader
            with open(path, "rb") as f:
                content = f.read()
            with upload.reader as f:
                self.assertEqual(content, f.read())

    def test_creating_file_upload_with_no_nexisting_file_fails(self):
        path = "this-file-does-not-exist.x"

        with pytest.raises(FileNotFoundError):
            self.anonymous_client.create_file_upload(path)

    def test_add_attachments(self):
        dataset_id = self._create_draft()

        uploads = [
            Upload(io.BytesIO(b"Content 1"), "test.txt", mime_type="text/plain"),
            Upload(io.BytesIO(b"Content 2"), "test.test", mime_type="text/x-test"),
        ]

        info = self.authorized_client.add_attachments(dataset_id, uploads)

        self.assertEqual(info[0].filename, "test.txt")
        self.assertEqual(info[1].filename, "test.test")
        self.assertIsInstance(info[0].sha256, str)
        self.assertIsInstance(info[1].sha256, str)

        # load 1st attachment metadata
        attachment = self.authorized_client.get_attachment(dataset_id, info[0].id)
        self.assertEqual(attachment.filename, "test.txt")
        self.assertEqual(attachment.mime_type, "text/plain")

        # load 2nd attachment metadata
        attachment = self.authorized_client.get_attachment(dataset_id, info[1].id)
        self.assertEqual(attachment.filename, "test.test")
        self.assertEqual(attachment.mime_type, "text/x-test")

        tests = [
            (info[0].id, b"Content 1"),
            (info[1].id, b"Content 2"),
        ]
        for attachment_id, content in tests:
            reader = self.authorized_client.get_attachment_reader(
                dataset_id, attachment_id
            )
            with reader as f:
                self.assertEqual(content, f.read())

    def test_adding_attachments_without_auth_fails(self):
        dataset_id = self._create_draft()

        uploads = [
            Upload(io.BytesIO(b"Content 1"), "test.txt", mime_type="text/plain"),
            Upload(io.BytesIO(b"Content 2"), "test.test", mime_type="text/x-test"),
        ]

        with pytest.raises(APIException):
            self.invalid_token_client.add_attachments(dataset_id, uploads)

    def test_add_attachment(self):
        dataset_id = self._create_draft()

        content = b"Content 3"
        upload = Upload(io.BytesIO(content), "test.txt", mime_type="text/plain")
        upload.title = "Custom title"
        upload.description = "Custom description"

        info = self.authorized_client.add_attachment(dataset_id, upload)

        self.assertEqual(info.filename, "test.txt")

        attachment = self.authorized_client.get_attachment(dataset_id, info.id)
        self.assertEqual(attachment.filename, "test.txt")
        self.assertEqual(attachment.mime_type, "text/plain")
        self.assertEqual(attachment.byte_size, len(content))
        self.assertEqual(attachment.title, "Custom title")
        self.assertEqual(attachment.description, "Custom description")
        self.assertIsInstance(attachment.released, datetime)

        reader = self.authorized_client.get_attachment_reader(dataset_id, info.id)
        with reader as f:
            self.assertEqual(content, f.read())

    def test_adding_attachment_without_auth_fails(self):
        dataset_id = self._create_draft()

        upload = Upload(io.BytesIO(b"Content 1"), "test.txt", mime_type="text/plain")

        with pytest.raises(MissingAccountException):
            self.anonymous_client.add_attachment(dataset_id, upload)

    # DELETE ATTACHMENT

    def test_delete_attachment(self):
        dataset_id = self._create_draft()
        attachment_id = self._create_attachment(dataset_id, b"Content 3")

        # delete attachment
        self.authorized_client.delete_attachment(dataset_id, attachment_id)

        # try to load attachment
        attachment = self.authorized_client.get_attachment(dataset_id, attachment_id)
        self.assertEqual(attachment, None)

    # UPDATE ATTACHMENT METADATA

    def test_update_attachment(self):
        dataset_id = self._create_draft()
        attachment_id = self._create_attachment(dataset_id, b"Content 3")

        # update and check

        updated_meta = {
            "description": "Custom description",
            "filename": "custom-filename.txt",
            "title": "Custom title",
        }

        attachment = self.authorized_client.update_attachment(
            dataset_id, attachment_id, **updated_meta
        )
        self.assertIsInstance(attachment, Attachment)
        self.assertEqual(attachment.description, updated_meta["description"])
        self.assertEqual(attachment.filename, updated_meta["filename"])
        self.assertEqual(attachment.title, updated_meta["title"])

        # load attachment again and check

        attachment = self.authorized_client.get_attachment(dataset_id, attachment_id)
        self.assertEqual(attachment.description, updated_meta["description"])
        self.assertEqual(attachment.filename, updated_meta["filename"])
        self.assertEqual(attachment.title, updated_meta["title"])

    # UPLOAD AND DOWNLOAD ATTACHMENTS AS FILES

    def test_upload_single_attachment(self):
        dataset_id = self._create_draft()

        filename = "upload-download.txt"

        with tempfile.TemporaryDirectory() as dir:
            path = os.path.join(dir, filename)

            # create local file
            content = b"File content"
            with open(path, "wb") as f:
                f.write(content)

            # upload file
            info = self.authorized_client.upload_attachment(dataset_id, path)

        self.assertIsInstance(info, UploadInfo)
        self.assertEqual(info.filename, filename)

    def test_download_single_attachment(self):
        filename = "upload-download.txt"
        content = b"File content"
        dataset_id = self._create_draft()
        attachment_id = self._create_attachment(dataset_id, content, filename)

        # download file

        with tempfile.TemporaryDirectory() as dir:
            path = os.path.join(dir, filename)

            path = self.authorized_client.download_attachment(
                dataset_id, attachment_id, dir
            )
            with open(path, "rb") as f:
                self.assertEqual(content, f.read())

    def test_upload_multiple_attachments(self):
        dataset_id = self._create_draft()
        files = self._file_tests

        with tempfile.TemporaryDirectory() as dir:
            # create local files
            paths = []
            for filename, content in files.items():
                path = os.path.join(dir, filename)
                paths.append(path)
                with open(path, "wb") as f:
                    f.write(content)

            # upload files
            info = self.authorized_client.upload_attachments(dataset_id, paths)

        want_filenames = list(files.keys())
        got_filenames = [i.filename for i in info]
        self.assertListEqual(want_filenames, got_filenames)

    def test_download_attachments_as_zip(self):
        dataset_id = self._create_draft()
        files = self._file_tests
        for filename, content in files.items():
            self._create_attachment(dataset_id, content, filename)

        with tempfile.TemporaryDirectory() as dir:
            path = self.authorized_client.download_attachments_as_zip(dataset_id, dir)

            self.assertEqual(path, f"{dir}/{dataset_id}_files.zip")
            self.assertTrue(zipfile.is_zipfile(path))

            zip_info = zipfile.ZipFile(path).infolist()
            # check the file names
            expected_filenames = files.keys()
            zip_filenames = [info.filename for info in zip_info]
            self.assertEqual(set(expected_filenames), set(zip_filenames))
            # check the content lengths
            expected_lengths = [len(content) for content in files.values()]
            zip_lengths = [info.file_size for info in zip_info]
            self.assertEqual(set(expected_lengths), set(zip_lengths))

    def test_download_attachments_as_zip_through_dataset_instance(self):
        dataset_id = self._create_draft()
        files = self._file_tests
        for filename, content in files.items():
            self._create_attachment(dataset_id, content, filename)

        dataset = self.authorized_client.get_dataset(dataset_id)
        self.assertIsInstance(dataset, Dataset)

        with tempfile.TemporaryDirectory() as dir:
            path = dataset.download_attachments_as_zip(dir)

            self.assertEqual(path, f"{dir}/{dataset_id}_files.zip")
            self.assertTrue(zipfile.is_zipfile(path))

    def test_downloading_attachments_as_zip_to_nonexisting_dir_fails(self):
        with pytest.raises(FileNotFoundError):
            self.authorized_client.download_attachments_as_zip(
                "some-id", "this-dir-does-not-exist.x"
            )

    def test_uploading_nonexisting_file_fails(self):
        with pytest.raises(FileNotFoundError):
            self.authorized_client.upload_attachment(
                "some-id", "this-file-does-not-exist.x"
            )

    def test_uploading_nonexisting_files_fails(self):
        with pytest.raises(FileNotFoundError):
            self.authorized_client.upload_attachments(
                "some-id", ["this-file-does-not-exist.x"]
            )

    def test_downloading_file_to_nonexisting_dir_fails(self):
        with pytest.raises(FileNotFoundError):
            self.authorized_client.download_attachment(
                "some-id", "some-id", "this-dir-does-not-exist.x"
            )

    def test_downloading_from_nonexisting_attachment_fails(self):
        path = self.authorized_client.download_attachment(
            self.PUBLIC_ID, str(uuid.uuid4()), "/tmp"
        )
        self.assertIsNone(path)


@pytest.mark.usefixtures("run_fixtures")
class TestPermission(unittest.TestCase):
    def setUp(self):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def test_create_permission(self):
        # cleanup
        try:
            self.authorized_client.delete_permission(self.DRAFT_ID, self.OTHER_USER_ID)
        except APIException:
            pass

        # add permission
        permission = self.authorized_client.add_permission(
            self.DRAFT_ID, self.OTHER_USER_ID, may_read=True, may_update=True
        )

        self.assertIsInstance(permission, Permission)
        self.assertTrue(permission.may_read)
        self.assertTrue(permission.may_update)
        self.assertFalse(permission.may_delete)
        self.assertEqual(permission.object_id, self.DRAFT_ID)
        self.assertEqual(permission.user_id, self.OTHER_USER_ID)

    def test_get_permissions(self):
        permissions = self.authorized_client.get_permissions(self.DRAFT_ID)

        self.assertIsInstance(permissions, PermissionCollection)

        executed = False
        for permission in permissions:
            self.assertIsInstance(permission, Permission)
            self.assertIsInstance(permission.user_id, str)
            self.assertIsInstance(permission.may_read, bool)
            self.assertIsInstance(permission.may_update, bool)
            self.assertIsInstance(permission.may_delete, bool)
            executed = True

        self.assertTrue(executed)

    def test_get_permission(self):
        permission = self.authorized_client.get_permission(
            self.DRAFT_ID, self.authorized_user_id
        )

        self.assertIsInstance(permission, Permission)
        self.assertEqual(permission.user_id, self.authorized_user_id)

    def test_getting_permission_with_invalid_object_id_fails(self):
        permission = self.authorized_client.get_permission(
            self.DRAFT_ID, str(uuid.uuid4())
        )

        self.assertIsNone(permission)

    def test_getting_permission_with_unauthorized_client_fails(self):
        with pytest.raises(APIException):
            self.invalid_token_client.get_permission(
                self.DRAFT_ID, self.authorized_user_id
            )

    def test_update_permission(self):
        # cleanup
        try:
            self.authorized_client.delete_permission(self.DRAFT_ID, self.OTHER_USER_ID)
        except APIException:
            pass

        # create permission
        self.authorized_client.add_permission(self.DRAFT_ID, self.OTHER_USER_ID)

        # update permission
        permission = self.authorized_client.update_permission(
            self.DRAFT_ID, self.OTHER_USER_ID, may_read=True
        )

        self.assertIsInstance(permission, Permission)
        self.assertTrue(permission.may_read)
        self.assertFalse(permission.may_update)
        self.assertFalse(permission.may_delete)
        self.assertEqual(permission.object_id, self.DRAFT_ID)
        self.assertEqual(permission.user_id, self.OTHER_USER_ID)

    def test_delete_permission(self):
        # cleanup
        try:
            self.authorized_client.delete_permission(self.DRAFT_ID, self.OTHER_USER_ID)
        except APIException:
            pass

        # create permission
        self.authorized_client.add_permission(self.DRAFT_ID, self.OTHER_USER_ID)

        # delete permission
        self.authorized_client.delete_permission(self.DRAFT_ID, self.OTHER_USER_ID)

        # try to read this permission
        result = self.authorized_client.get_permission(
            self.DRAFT_ID, self.OTHER_USER_ID
        )
        self.assertIsNone(result)


class TestMissingClientException(unittest.TestCase):
    # in these tests Dataset and Attachment objects are created manually. This
    # should never be done manually in production code.

    def test_fail_to_call_attachment_methods_that_need_a_client(self):
        raw = dict(
            byteSize=0,
            created=datetime.now().isoformat(),
            createdBy="",
            datasetId="",
            description="",
            filename="",
            id="",
            mimeType="",
            modified=datetime.now().isoformat(),
            modifiedBy="",
            released=datetime.now().isoformat(),
            sha256="",
            title="",
        )

        attachment = Attachment(raw)

        with pytest.raises(MissingClientException):
            attachment.reader()

    def test_fail_to_call_dataset_methods_that_need_a_client(self):
        raw = dict(
            content={},
            created=datetime.now().isoformat(),
            createdBy="",
            doi="",
            id="",
            modified=datetime.now().isoformat(),
            modifiedBy="",
            published=datetime.now().isoformat(),
            publishedBy="",
            type=DatasetType.DRAFT,
        )

        dataset = Dataset(raw)

        with pytest.raises(MissingClientException):
            dataset.get_attachments()

        with pytest.raises(MissingClientException):
            dataset.download_attachments_as_zip("")
