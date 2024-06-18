import logging
import pendulum

from authlib.integrations.requests_client import OAuth2Session
from authlib.jose import jwt
from authlib.jose.errors import (
    JoseError,
    DecodeError,
    BadSignatureError,
    ExpiredTokenError,
    InvalidClaimError,
)
from requests.exceptions import HTTPError

from .config import (
    AUTHORIZATION_URL,
    DOMAIN,
    GET_USER_DATA_URL,
    TEST_DOMAIN,
    TOKEN_ISSUE_URL,
)
from .utils import validate_token


class KidOAuth2Client:
    def __init__(
        self, client_id: str, client_secret: str, redirect_uri: str, test: bool = False
    ):
        """
        Initializes the OAuth2 client.

        :param client_id: Client identifier
        :param client_secret: Client secret
        :param redirect_uri: Redirect URI
        :param test: Boolean indicating whether to use the test domain
        """
        self.redirect_uri = redirect_uri
        self.session = OAuth2Session(
            client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri
        )
        self.token = None
        self.token_expires_at = None
        self.domain = TEST_DOMAIN if test else DOMAIN
        self.authorization_url = AUTHORIZATION_URL.format(domain=self.domain)
        self.token_issue_url = TOKEN_ISSUE_URL.format(domain=self.domain)
        self.get_user_data_url = GET_USER_DATA_URL.format(domain=self.domain)

    @property
    def token_is_expired(self) -> bool:
        if self.token_expires_at is None:
            return True
        return pendulum.now("UTC").timestamp() >= self.token_expires_at

    def get_authorization_url(self) -> str:
        """
        Creates an authorization URL.

        :return: Authorization URL
        """
        return self.session.create_authorization_url(
            self.authorization_url, redirect_uri=self.redirect_uri
        )[0]

    def fetch_token(self, code: str) -> str:
        """
        Fetches the access token.

        :param code: Authorization code
        :return: Access token
        :raises Exception: If there is an error fetching the token
        """
        try:
            self.token = self.session.fetch_token(self.token_issue_url, code=code)
        except Exception as e:
            logging.error(f"Error fetching token: {e}")
            raise

        self.token_expires_at = self.token["expires_at"]
        return self.token["access_token"]

    @validate_token
    def get_user_data(self) -> dict:
        """
        Retrieves user data using the token.

        :return: Dictionary containing user data
        :raises HTTPError: If the request fails
        """
        self.session.token = self.token

        try:
            response = self.session.get(self.get_user_data_url)
            response.raise_for_status()
        except HTTPError as http_err:
            logging.error(f"HTTP error occurred: {http_err}")
            raise
        except Exception as err:
            logging.error(f"Error occurred: {err}")
            raise

        return response.json()


class KidJWTClient:
    @staticmethod
    def parse_jwt(encoded_jwt: str, key: str) -> dict:
        """
        Parses a JWT token.

        :param encoded_jwt: Encoded JWT token
        :param key: Key for decoding
        :return: Dictionary containing claims or None if an error occurs
        """
        try:
            claims = jwt.decode(encoded_jwt, key)
            claims.validate()
        except DecodeError as e:
            logging.error(f"Failed to decode JWT: {e}")
            raise e
        except BadSignatureError as e:
            logging.error(f"Invalid signature: {e}")
            raise e
        except ExpiredTokenError as e:
            logging.error(f"Token has expired: {e}")
            raise e
        except InvalidClaimError as e:
            logging.error(f"Invalid claim: {e}")
            raise e
        except JoseError as e:
            logging.error(f"Failed to decode JWT: {e}")
            raise e

        if not isinstance(claims, dict):
            logging.error("Claims data is not a dictionary")
            raise TypeError("Claims data is not a dictionary")

        return claims
