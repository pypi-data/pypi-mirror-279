from __future__ import annotations
import base64
import requests
from typing import Optional

from .exception import APIException
from .types import (
    AccessLevel,
    AccountAPIResponse,
    AccountWithTokenAPIResponse,
    KeepaliveAPIResponse,
)

AUTH_STAGING_ENTRYPOINT = "https://beta.data.npolar.no/-/auth/"
AUTH_LIFE_ENTRYPOINT = "https://auth.data.npolar.no/"


class Account:
    """
    A basic account object.

    Attributes:
        raw (AccountAPIResponse): The API response data parsed from JSON
        client (AuthClient | None): The client for the auth module
    """

    client: Optional[AuthClient]
    access_level: AccessLevel
    directory_user: bool
    email: str
    id: str

    def __init__(
        self, raw: AccountAPIResponse, *, client: Optional[AuthClient] = None
    ) -> None:
        """
        Initialize an instance of the Account model class.

        Args:
            raw (AccountAPIResponse): The API response as parsed JSON
            client (AuthClient): The used auth client
        """
        self.client = client
        self.access_level = AccessLevel(raw["accessLevel"])
        self.directory_user = raw.get("directoryUser", False)
        self.email = raw["email"]
        self.id = raw["id"]


class AuthContainer:
    """
    A container that can be used for authentification.

    Attributes:
        token (str): the auth token used for authentification

    """

    token: str

    def __init__(self, token: str) -> None:
        """
        Initialize an instance of the AuthContainer class.

        Args:
            token (str): the auth token used for authentification
        """
        self.token = token

    @property
    def headers(self) -> dict[str, str]:
        """
        Retreive the header(s) for an authorized HTTP request

        Returns:
            dict[str, str]: The auth headers
        """
        return {"Authorization": f"Bearer {self.token}"}


class AccountWithToken(AuthContainer, Account):
    """
    A logged in account with token. Inherits from AuthContainer and Account

    Attributes:
        raw (AccountWithTokenAPIResponse): The API response data parsed from JSON
        client (AuthClient | None): The client for the auth module
    """

    raw: AccountWithTokenAPIResponse

    def __init__(
        self, raw: AccountWithTokenAPIResponse, *, client: Optional[AuthClient] = None
    ) -> None:
        """
        Initialize an instance of the AccountWithToken model class.

        Args:
            raw (AccountWithTokenAPIResponse): The API response as parsed JSON
            client (AuthClient): The used auth client
        """

        Account.__init__(self, raw, client=client)
        AuthContainer.__init__(self, raw["token"])


class AuthClient:
    entrypoint: str
    verify_ssl: bool

    """
    A client to communicate with the NPDC auth module.

    Attributes:
        entrypoint (str): The entrypoint of the Rest API with a trailing slash
        verify_ssl (bool): Set to false, when the Rest API has a self signed
            certificate
    """

    def __init__(self, entrypoint: str, *, verify_ssl: bool = True) -> None:
        """
        Create a new AuthClient.

        Args:
            entrypoint (str): The entrypoint of the Rest API with a trailing
                slash
            verify_ssl (bool): Set to false, when the Rest API has a self signed
                certificate
        """
        self.entrypoint = entrypoint
        self.verify_ssl = verify_ssl

    def login(self, email: str, password: str) -> AccountWithToken:
        """
        Login a user and retrieve account.

        Args:
            email (str): The user email
            password (str): The user password

        Returns:
            AccountWithToken: The logged in account

        Raises:
            APIException: if the HTTP status code of the response is not 200
        """
        creds = base64.b64encode(bytes(f"{email}:{password}", "utf8"))
        endpoint = f"{self.entrypoint}authenticate/"
        headers = {"Authorization": "Basic " + creds.decode("utf8")}

        response = requests.get(endpoint, headers=headers, verify=self.verify_ssl)
        if response.status_code != 200:
            raise APIException(response)

        return AccountWithToken(response.json(), client=self)

    def logout(self, auth: AuthContainer) -> None:
        """
        Logout a user.

        Args:
            auth (AuthContainer): An object containing the auth token

        Raises:
            APIException: if the HTTP status code of the response is not 200
        """
        endpoint = f"{self.entrypoint}authenticate/"
        response = requests.delete(
            endpoint, headers=auth.headers, verify=self.verify_ssl
        )
        if response.status_code != 200:
            raise APIException(response)

    def authorize(self, auth: AuthContainer) -> Account:
        """
        Retrieve a logged in account by token

        Args:
            auth (AuthContainer): An object containing the auth token

        Returns:
            Account

        Raises:
            APIException: if the HTTP status code of the response is not 200
        """

        endpoint = f"{self.entrypoint}authorize/"
        response = requests.get(endpoint, headers=auth.headers, verify=self.verify_ssl)

        if response.status_code != 200:
            raise APIException(response)

        return Account(response.json())

    def create_account(
        self, auth: AuthContainer, email: str, link_prefix: str
    ) -> Account:
        """
        Create a new external account

        Only admins have access to this method

        Args:
            auth (AuthContainer): the account used to create the new
                account. Has to have accessLevel admin.
            email (str): the email for the account. The email domain must not be
                an internal one (npolar.no in the production system)
            link_prefix (str): the link prefix. Used to build a URL in the
                email.

        Returns:
            Account

        Raises:
            APIException: if the HTTP status code of the response is not 201
        """

        endpoint = f"{self.entrypoint}account/"
        payload = {"email": email, "linkPrefix": link_prefix}
        response = requests.post(
            endpoint, headers=auth.headers, json=payload, verify=self.verify_ssl
        )

        if response.status_code != 201:
            raise APIException(response)

        return Account(response.json())

    def get_account(self, account_id: str) -> Account | None:
        """
        Retrieve an account by ID

                When the account is not found, None is returned.

        Args:
            account_id (str): the UUID of the account

        Returns:
            Account | None

        Raises:
            APIException: if the HTTP status code of the response is 500
        """

        endpoint = f"{self.entrypoint}account/{account_id}"
        response = requests.get(endpoint, verify=self.verify_ssl)

        if response.status_code == 404:
            return None
        if response.status_code != 200:
            raise APIException(response)

        return Account(response.json())

    def update_account(
        self, auth: AuthContainer, account_id: str, *, active: bool
    ) -> Account:
        """
        Update an external account

        Only admins have access to this method

        Args:
            auth (AuthContainer): the account used to update the account. Has
                to have accessLevel admin.
            account_id (str): the UUID of the account
            active (bool): the active set to be updated in the account

        Returns:
            Account

        Raises:
            APIException: if the HTTP status code of the response is not 200
        """

        endpoint = f"{self.entrypoint}account/{account_id}"
        payload = {"active": active}
        response = requests.put(
            endpoint, headers=auth.headers, json=payload, verify=self.verify_ssl
        )

        if response.status_code != 200:
            raise APIException(response)

        return Account(response.json())

    def change_password(
        self, auth: AuthContainer, current_password: str, new_password: str
    ) -> None:
        endpoint = f"{self.entrypoint}account/"
        payload = {
            "currentPassword": current_password,
            "newPassword": new_password,
        }

        response = requests.put(
            endpoint, headers=auth.headers, json=payload, verify=self.verify_ssl
        )
        if response.status_code > 204:
            raise APIException(response)

    def keepalive(self, auth: AuthContainer) -> str:
        """
        Extend the login session and retrieve a new token

        Args:
            auth (AuthContainer): the account that should be extended. Has
                to have a valid token

        Returns:
            str

        Raises:
            APIException: if the HTTP status code of the response is not 200
        """
        endpoint = f"{self.entrypoint}keepalive/"

        response = requests.post(endpoint, headers=auth.headers, verify=self.verify_ssl)

        if response.status_code != 200:
            raise APIException(response)

        response_data: KeepaliveAPIResponse = response.json()
        return response_data["token"]
