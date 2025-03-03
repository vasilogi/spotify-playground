import spotipy
from spotipy.oauth2 import SpotifyOAuth
from types import TracebackType
from typing import Optional, Type

# Custom modules
from .exceptions import (
    SpotifyAPIError,
    AuthenticationError,
    InvalidParameterError,
    UnexpectedAuthenticationError,
)

class SpotifyClient:

    def __init__(
            self,
            client_id: str,
            client_secret: str,
            redirect_uri: str,
            scope: str
    ):
        self.client_id: str = client_id
        self.client_secret: str = client_secret
        self.redirect_uri: str = redirect_uri
        self.scope: str = scope
        self.client: Optional[spotipy.Spotify] = None

    def __enter__(self) -> spotipy.Spotify:
        return self.create_spotify_client()
    
    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType]
    ) -> None:
        if self.client:
            self.close()

    def create_spotify_client(self) -> spotipy.Spotify:
        try:
            auth_manager=SpotifyOAuth(
                client_id=self.client_id,
                client_secret=self.client_secret,
                redirect_uri=self.redirect_uri,
                scope=self.scope
            )
            self.client = spotipy.Spotify(auth_manager=auth_manager)
            return self.client
        except spotipy.SpotifyOauthError as e:
            raise AuthenticationError(f"OAuth authentication error: {e}") from e
        except spotipy.SpotifyException as e:
            raise SpotifyAPIError(f"Spotify API error: {e}") from e
        except ValueError as e:
            raise InvalidParameterError(f"Invalid parameter error: {e}") from e
        except Exception as e:
            raise UnexpectedAuthenticationError(f"Unexpected error during authentication: {e}") from e
        
    def close(self) -> None:
        if self.client:
            # Clear the token
            self.client.auth_manager.token_info = None
            self.client = None
