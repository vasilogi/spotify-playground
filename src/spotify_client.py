import logging
from types import TracebackType
from typing import Optional, Type

import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Custom modules
from .exceptions import (
    SpotifyAPIError,
    AuthenticationError,
    InvalidParameterError,
    UnexpectedAuthenticationError,
)

class SpotifyClient:
    """A client for interacting with the Spotify API."""

    def __init__(
            self,
            client_id: str,
            client_secret: str,
            redirect_uri: str,
            scope: str
    ):
        """
        Initialize the SpotifyClient.

        :param client_id: Spotify API client ID
        :param client_secret: Spotify API client secret
        :param redirect_uri: Redirect URI for OAuth flow
        :param scope: Spotify API scope (default: "user-library-read")
        """
        self.client_id: str = client_id
        self.client_secret: str = client_secret
        self.redirect_uri: str = redirect_uri
        self.scope: str = scope
        self._client: Optional[spotipy.Spotify] = None
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)

    def __enter__(self) -> spotipy.Spotify:
        """Enter the runtime context and return the Spotify client."""
        return self.client
    
    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType]
    ) -> bool:
        try:
            self.close()
        except Exception as e:
            self.logger.error(f"Error during SpotifyClient cleanup: {e}")
        return False # Propagate exceptions
    
    @property
    def client(self) -> spotipy.Spotify:
        """Lazy initialization of the Spotify client."""
        if self._client is None:
            self._client = self.create_spotify_client()
        return self._client

    def create_spotify_client(self) -> spotipy.Spotify:
        """Create and return a new Spotify client."""
        try:
            auth_manager=SpotifyOAuth(
                client_id=self.client_id,
                client_secret=self.client_secret,
                redirect_uri=self.redirect_uri,
                scope=self.scope
            )
            return spotipy.Spotify(auth_manager=auth_manager)
        except spotipy.SpotifyOauthError as e:
            raise AuthenticationError(f"OAuth authentication error: {e}") from e
        except spotipy.SpotifyException as e:
            raise SpotifyAPIError(f"Spotify API error: {e}") from e
        except ValueError as e:
            raise InvalidParameterError(f"Invalid parameter error: {e}") from e
        except Exception as e:
            raise UnexpectedAuthenticationError(f"Unexpected error during authentication: {e}") from e
        
    def close(self) -> None:
        """Close the Spotify client and clear authentication."""
        if self._client:
            self.logger.info("Closing Spotify client and clearing authentication")
            self._client.auth_manager.token_info = None
            self._client = None
