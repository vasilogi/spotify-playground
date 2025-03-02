from typing import List, Dict, Any
import pandas as pd
from tqdm import tqdm
import spotipy

# Custom modules
from .exceptions import (
    SpotifyAPIError,
    FileWriteError,
    UnexpectedError
)


class DataFetcher:

    def __init__(self, spotify_client: spotipy.Spotify):
        self.sp: spotipy.Spotify = spotify_client
        self.pagination_limit: int = 50


    def calculate_total_albums(self) -> int:
        
        limit: int = 1
        
        try:
            results: Dict[str, Any] = self.sp.current_user_saved_albums(limit=limit)
        except spotipy.SpotifyException as e:
            raise SpotifyAPIError(f"Failed to fetch albums: {e}") from e
        
        return results['total']

    
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