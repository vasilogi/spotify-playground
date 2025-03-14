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
    UnexpectedError
)

class SpotifyClient:
    """
    A wrapper class for the Spotify API client that provides simplified authentication
    and error handling.

    This class implements the context manager protocol, allowing it to be used with
    the 'with' statement. It also uses lazy initialization, so the actual Spotify
    client is only created when needed.

    Attributes:
        client_id (str): The Spotify API client ID.
        client_secret (str): The Spotify API client secret.
        redirect_uri (str): The URI to redirect to after authentication.
        scope (str): The permission scopes to request from Spotify.

    Examples:
        Basic usage with context manager:
        
        ```
        from spotify_utils import SpotifyClient
        
        # Create the client with your Spotify API credentials
        with SpotifyClient(
            client_id="your_client_id",
            client_secret="your_client_secret",
            redirect_uri="http://localhost:8888/callback"
        ) as spotify:
            # 'spotify' is now a spotipy.Spotify instance
            results = spotify.search(q="Radiohead", type="artist")
            for artist in results['artists']['items']:
                print(artist['name'])
        ```
        
        Using the client without a context manager:
        
        ```
        spotify_wrapper = SpotifyClient(
            client_id="your_client_id",
            client_secret="your_client_secret",
            redirect_uri="http://localhost:8888/callback",
            scope="user-library-read user-top-read"
        )
        
        # Access the client property to initialize the Spotify client
        spotify = spotify_wrapper.client
        
        # Use the Spotify API
        saved_tracks = spotify.current_user_saved_tracks(limit=10)
        for item in saved_tracks['items']:
            track = item['track']
            print(f"{track['name']} by {track['artists']['name']}")
        ```
    """

    def __init__(
            self,
            client_id: str = None,
            client_secret: str = None,
            redirect_uri: str = None,
            scope: str = "user-library-read"
    ):
        """
        Initialize the SpotifyClient with the provided credentials.
        
        The actual Spotify client is not created until needed (lazy initialization).
        
        Args:
            client_id (str, optional): The Spotify API client ID. Defaults to None.
            client_secret (str, optional): The Spotify API client secret. Defaults to None.
            redirect_uri (str, optional): The URI to redirect to after authentication.
                                        Defaults to None.
            scope (str, optional): Space-separated list of Spotify permission scopes. 
                                  Defaults to "user-library-read".
        
        Note:
            If any of the required credentials are not provided, they will be looked up
            from environment variables when the Spotify client is created.
        """
        self.client_id: str = client_id
        self.client_secret: str = client_secret
        self.redirect_uri: str = redirect_uri
        self.scope: str = scope
        self._client: Optional[spotipy.Spotify] = None

    def __enter__(self) -> spotipy.Spotify:
        """
        Enter the runtime context for the SpotifyClient.
        
        This method is called when entering a 'with' statement and triggers
        lazy initialization of the Spotify client.
        
        Returns:
            spotipy.Spotify: The initialized Spotify client.
        """
        return self.client

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        exc_traceback: Optional[TracebackType]
    ) -> bool:
        """
        Exit the runtime context for the SpotifyClient.
        
        This method is called when exiting a 'with' statement. It cleans up
        the Spotify client by clearing token information and setting the client to None.
        
        Args:
            exc_type: The exception type if an exception was raised in the with block,
                    None otherwise.
            exc_value: The exception instance if an exception was raised, None otherwise.
            exc_traceback: The traceback if an exception was raised, None otherwise.
            
        Returns:
            bool: False to indicate that exceptions should be propagated.
            
        Raises:
            UnexpectedError: If an error occurs during cleanup.
        """
        try:
            if self._client is not None:
                self._client.auth_manager.token_info = None
                self._client = None
        except Exception as e:
            raise UnexpectedError(f"Unexpected error while exiting: {e}") from e
        return False

    @property
    def client(self) -> spotipy.Spotify:
        """
        Get the Spotify client, creating it if it doesn't exist yet.
        
        This property implements lazy initialization, creating the Spotify client
        only when first accessed.
        
        Returns:
            spotipy.Spotify: The initialized Spotify client.
            
        Raises:
            Various exceptions from create_spotify_client() if initialization fails.
        """
        if self._client is None:
            self._client = self.create_spotify_client()
        return self._client

    def create_spotify_client(self) -> spotipy.Spotify:
        """
        Create and initialize a new Spotify client with OAuth authentication.
        
        This method handles the actual creation of the Spotify client and wraps
        any exceptions in more specific exception types.
        
        Returns:
            spotipy.Spotify: The newly created Spotify client.
            
        Raises:
            AuthenticationError: If OAuth authentication fails.
            SpotifyAPIError: If there's an error with the Spotify API.
            InvalidParameterError: If any of the parameters are invalid.
            UnexpectedAuthenticationError: For any other unexpected errors during authentication.
        """
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
            raise UnexpectedAuthenticationError(
                f"Unexpected error during authentication: {e}"
            ) from e
