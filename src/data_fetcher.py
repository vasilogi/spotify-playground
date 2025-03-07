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
    
    def calculate_total_playlists(self) -> int:
        
        limit: int = 1
        
        try:
            results: Dict[str, Any] = self.sp.current_user_playlists(limit=limit)
        except spotipy.SpotifyException as e:
            raise SpotifyAPIError(f"Failed to fetch playlists: {e}") from e
        
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
        
    def fetch_all_playlists(self, csv_filepath: str) -> None:
        
        total_playlists: int = self.calculate_total_playlists()
        play_lists: List[Dict[str, Any]] = []
        offset: int = 0
        limit: int = self.pagination_limit
        
        with tqdm(total=total_playlists, desc='Fetching all playlists') as pbar:
            # loop over all current user playlists
            while True:
                current_user_playlists: Dict[str, Any] = self.sp.current_user_playlists(limit=limit, offset=offset)
                playlists: Dict[str, Any] = current_user_playlists['items']
                # exit the loop if no playlists are found
                if not playlists:
                    break
                # loop over playlists
                for playlist in playlists:
                    play_lists.append(
                        {
                            'Playlist Name': playlist['name'],
                            'Playlist ID': playlist['id']
                        }
                    )

                # Update offset and progress bar
                offset += limit
                pbar.update(len(current_user_playlists['items']))

            # Save dataframe into a CSV
            df: pd.DataFrame = pd.DataFrame(play_lists)
            try:
                df.to_csv(csv_filepath, index=False)
                print(f"All Playlists dataFrame successfully saved in {csv_filepath}.")
            except IOError as e:
                raise FileWriteError("Unable to write all playlists to the CSV file: {e}") from e
            except Exception as e:
                raise UnexpectedError(
                    f"An unexpected error occured while writing all playlists to the CSV: {e}"
                ) from e


    # def fetch_tracks_from_playlist(self):
    #     pass