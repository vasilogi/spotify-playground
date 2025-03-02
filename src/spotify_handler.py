import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
from tqdm import tqdm
from typing import List, Dict, Any
from .exceptions import (
    SpotifyAPIError,
    AuthenticationError,
    InvalidParameterError,
    UnexpectedAuthenticationError,
    FileWriteError,
    UnexpectedError
)


class SpotifyAPI:

    def __init__(self, client_id: str, client_secret: str, redirect_uri: str):
        self.client_id: str = client_id
        self.client_secret: str = client_secret
        self.redirect_uri: str = redirect_uri
        self.sp: spotipy.Spotify | None = None
        self.pagination_limit: int = 50

    def connect(self, scope: str) -> bool:
        try:
            self.sp = spotipy.Spotify(
                auth_manager=SpotifyOAuth(
                    client_id=self.client_id,
                    client_secret=self.client_secret,
                    redirect_uri=self.redirect_uri,
                    scope=scope
                )
            )
            print("User authenticated successfully.")
            return True
        except spotipy.SpotifyOauthError as e:
            raise AuthenticationError(f"OAuth authentication error: {e}") from e
        except spotipy.SpotifyException as e:
            raise SpotifyAPIError(f"Spotify API error: {e}") from e
        except ValueError as e:
            raise InvalidParameterError(f"Invalid parameter error: {e}") from e
        except Exception as e:
            raise UnexpectedAuthenticationError(f"Unexpected error during authentication: {e}") from e

    def calculate_total_albums(self) -> int:
        total_albums: int = 0
        offset: int = 0
        limit: int = self.pagination_limit
        
        print("Calculate total number of saved albums...")
        # Paginate through all saved albums
        while True:
            results: Dict[str, Any] = self.sp.current_user_saved_albums(limit=limit, offset=offset)
            # add the number of albums in the current page to the total
            total_albums += len(results['items'])

            # check if there are no more tracks (items) in the page
            if not results['items']:
                break

            # update the offset
            offset += limit

        return total_albums

    
    def fetch_all_albums(self, csv_filepath: str) -> None:

        total_albums: int = self.calculate_total_albums()
        albums: List[Dict[str, Any]] = []
        offset: int = 0
        limit: int = self.pagination_limit
        with tqdm(total=total_albums, desc='Fetching all albums') as pbar:
            while True:
                try:
                    results: Dict[str, Any] = self.sp.current_user_saved_albums(limit=limit, offset=offset)
                except spotipy.SpotifyException as e:
                    raise SpotifyAPIError(f"Failed to fetch albums: {e}") from e
                if not results['items']:
                    break
                for item in results['items']:
                    album: Dict[str, Any] = item['album']
                    albums.append({
                        'Album Name': album['name'],
                        'Artists': ", ".join(artist['name'] for artist in album['artists']),
                        'Release Date': album['release_date'],
                        'Popularity': album['popularity'],
                        'Image URL': album['images'][0]['url']
                    })
                
                # Update offset and progress bar
                offset += limit
                pbar.update(len(results['items']))

        # Save dataframe into a CSV
        df: pd.DataFrame = pd.DataFrame(albums)
        try:
            df.to_csv(csv_filepath, index=False)
            print(f"All Albums dataFrame successfully saved in {csv_filepath}.")
        except IOError as e:
            raise FileWriteError("Unable to write to the CSV file: {e}") from e
        except Exception as e:
            raise UnexpectedError(f"An unexpected error occured while writing the CSV: {e}") from e


    # def fetch_tracks_from_playlist(self):
    #     pass