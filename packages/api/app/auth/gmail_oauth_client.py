import json
import os
from typing import Any

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from oauthlib.oauth2 import InvalidGrantError
from requests import Request


class GmailOAuthClient:
    def __init__(
        self, credentials_file: str, token_file: str, scopes: list, redirect_uri: str
    ) -> None:
        self.credentials_file = credentials_file
        self.token_file = token_file
        self.scopes = scopes
        self.redirect_uri = redirect_uri

        # Ensure tokens directory exist
        os.makedirs(os.path.dirname(token_file), exist_ok=True)

    def get_authorisation_url(self) -> tuple[Any, Any]:
        try:
            flow = Flow.from_client_secrets_file(
                client_secrets_file=self.credentials_file, scopes=self.scopes
            )
            flow.redirect_uri = self.redirect_uri
            authorization_url, state = flow.authorization_url(
                access_type="offline", include_granted_scopes="true", prompt="consent"
            )
            return authorization_url, state
        except FileNotFoundError:
            raise ValueError(f"Credentials file not found: {self.credentials_file}")

    def exchange_code_for_token(self, code: str, state: str) -> dict:

        try:
            flow = Flow.from_client_secrets_file(
                client_secrets_file=self.credentials_file, scopes=self.scopes, state=state
            )
            flow.redirect_uri = self.redirect_uri
            flow.fetch_token(code=code)
            credentials = flow.credentials

            token_data = {
                "token": credentials.token,
                "refresh_token": credentials.refresh_token,
                "token_uri": credentials.token_uri,
                "client_id": credentials.client_id,
                "client_secret": credentials.client_secret,
                "scopes": credentials.scope,
            }
            self._save_token(token_data)
            return token_data
        except InvalidGrantError:
            raise ValueError("Invalid authorization code or code already used")
        except Exception as e:
            raise ValueError(f"Failed to exchange authorisation code for token: {e!s}")

    def get_credentials(self) -> Credentials:
        # Check if token file exists
        if not os.path.exists(self.token_file):
            raise FileNotFoundError(
                f"Token file not found: {self.token_file}. User needs to complete OAuth flow first."
            )

        try:
            with open(self.token_file) as f:
                token_data = json.load(f)

            credentials = Credentials(
                token=token_data.get("token"),
                refresh_token=token_data.get("refresh_token"),
                token_uri=token_data.get("token_uri"),
                client_id=token_data.get("client_id"),
                client_secret=token_data.get("client_secret"),
                scopes=token_data.get("scopes"),
            )

            if credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())

            refreshed_token_data = {
                "token": credentials.token,
                "refresh_token": credentials.refresh_token,
                "token_uri": credentials.token_uri,
                "client_id": credentials.client_id,
                "client_secret": credentials.client_secret,
                "scopes": credentials.scopes,
            }
            self._save_token(refreshed_token_data)
            return credentials
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid token file format: {e!s}")
        except Exception as e:
            raise ValueError(f"Failed to load or refresh credentials: {e!s}")

    # TODO: enforce atomic write to prevent corruption
    def _save_token(self, token_data: dict):
        try:
            os.makedirs(os.path.dirname(self.token_file), exist_ok=True)

            with open(self.token_file, "w") as f:
                json.dump(token_data, f, indent=2)

                # Set restrictive permissions (owner read/write only)
                os.chmod(self.token_file, 0o600)

        except OSError as e:
            raise OSError(f"Failed to save token to {self.token_file}: {e!s}")
