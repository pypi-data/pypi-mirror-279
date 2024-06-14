import os
import httpx
import toml
import logging

from pyhectiqlab import API_URL
from pathlib import Path
from typing import Optional, Union


def load_credentials(name: Optional[str] = None) -> Union[None, str]:
    path = os.getenv("HECTIQLAB_CREDENTIALS", os.path.join(Path.home(), ".hectiq-lab", "credentials.toml"))
    if not os.path.exists(path):
        return None
    with open(path, "r") as path:
        data = toml.load(path)
    # If key_name is provided, we return the value of the key_name
    if name is not None:
        return data[name]
    # Otherwise, we return the first value that is not None
    if len(data) > 0:
        return next(iter(data.values()))
    return None


def is_authenticated(name: Optional[str] = None) -> bool:
    """Checks if local is authenticated to the Hectiq Lab.
    If API key is None, the api_key is taken from:
     - the api_key located in the file `~/.hectiq-lab/credentials.toml`
     (or the HECTIQLAB_CREDENTIALS).

    Args:
        name (Optional[str], optional): Name of the API key. If None, the first available key is used.
            Default: None.

    Returns:
        bool: True if the user is authenticated, False otherwise.
    """

    data = load_credentials(name)
    if data is None:
        return False
    key = data.get("value")
    if key is None:
        return False
    return True


class Auth(httpx.Auth):
    """Authentication class for the Hectiq Lab API. This class is used to authenticate
    via an access token that is refreshed when it expires."""

    def __init__(self, name: Optional[str] = None):
        super().__init__()
        self.data = load_credentials(name)
        self.access_token = None
        self.refresh_token()

    def is_logged(self):
        return is_authenticated()

    @property
    def online(self):
        return self.access_token is not None

    @property
    def user(self):
        return self.data.get("user")

    @property
    def api_key(self):
        return os.getenv("HECTIQLAB_API_KEY") or self.data.get("value")

    @property
    def auth_header(self):
        return {"X-API-Key": self.api_key} if self.api_key else {}

    @property
    def auth_token_header(self):
        return {"Authentification": f"Bearer {self.access_token}"} if self.access_token is not None else {}

    def refresh_token(self):
        response = httpx.post(f"{API_URL}/app/auth/auth-api-key", headers=self.auth_header)
        if response.status_code != 200:
            logging.error("User could not be authenticated. Continuing in offline mode.")
            return
        self.access_token = response.cookies["access_token"]

    def auth_flow(self, request: httpx.Request):
        request.headers.update(self.auth_token_header)
        response = yield request

        if response.status_code == 401 or response.status_code == 403:
            response = yield self.build_refresh_request()
            self.access_token = response.cookies["access_token"]
            request.headers.update(self.auth_token_header)
            response = yield request

    def build_refresh_request(self):
        return httpx.Request("POST", f"{API_URL}/app/auth/auth-api-key", headers=self.auth_header)
