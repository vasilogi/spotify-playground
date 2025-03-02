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

    def create_spotify_client(self) -> spotipy.Spotify:
        try:
            return spotipy.Spotify(
                auth_manager=SpotifyOAuth(
                    client_id=self.client_id,
                    client_secret=self.client_secret,
                    redirect_uri=self.redirect_uri,
                    scope=self.scope
                )
            )
        except spotipy.SpotifyOauthError as e:
            raise AuthenticationError(f"OAuth authentication error: {e}") from e
        except spotipy.SpotifyException as e:
            raise SpotifyAPIError(f"Spotify API error: {e}") from e
        except ValueError as e:
            raise InvalidParameterError(f"Invalid parameter error: {e}") from e
        except Exception as e:
            raise UnexpectedAuthenticationError(f"Unexpected error during authentication: {e}") from e