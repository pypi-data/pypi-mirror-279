from enum import Enum
from typing import Any, Dict, TypedDict, Union


class AccessLevel(Enum):
    """
    The access level of an account

    Attributes:
        EXTERNAL  enum value for an external user
        INTERNAL  enum value for an internal user with a @npolar.no email address
        ADMIN     enum value for an admin user
    """

    EXTERNAL = "external"
    INTERNAL = "internal"
    ADMIN = "admin"


class AccountAPIResponse(TypedDict):
    id: str
    email: str
    accessLevel: AccessLevel
    directoryUser: bool


class AccountWithTokenAPIResponse(AccountAPIResponse):
    token: str


class KeepaliveAPIResponse(TypedDict):
    token: str


DatasetContent = Dict[str, Any]


class PermissionAPIResponse(TypedDict):
    objectId: str
    userId: str
    mayDelete: bool
    mayRead: bool
    mayUpdate: bool


class BaseModelAPIResponse(TypedDict):
    created: str
    createdBy: str
    id: str
    modified: str
    modifiedBy: str
    permissions: PermissionAPIResponse


class AttachmentAPIResponse(BaseModelAPIResponse):
    byteSize: int
    datasetId: str
    description: str
    filename: str
    mimeType: str
    released: str
    sha256: str
    title: str


class DatasetAPIResponse(BaseModelAPIResponse):
    content: DatasetContent
    doi: Union[str, None]
    published: str
    publishedBy: str
    type: str


class UploadInfoAPIResponse(TypedDict):
    id: str
    fileName: str
    sha256: str
