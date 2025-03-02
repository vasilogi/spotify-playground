import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd


class SpotifyAPI:

    def __init__(self, client_id, client_secret, redirect_uri):
        self.client_id=client_id
        self.client_secret=client_secret
        self.redirect_uri=redirect_uri
        self.sp = None

    def spotify_client(self, scope: str) -> None:
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
            return None
        except spotipy.SpotifyOauthError as e:
            print(f"OAuth authentication error: {e}")
        except spotipy.SpotifyException as e:
            print(f"Spotify API error: {e}")
        except ValueError as e:
            print(f"Invalid parameter error: {e}")
        except Exception as e:
            print(f"Unexpected error during authentication: {e}")

    
    def fetch_all_albums(self, csv_filepath: str) -> None:
        play_lists = []
        offset = 0
        # loop over all current user playlists
        while True:
            current_user_playlists = self.sp.current_user_playlists(limit=50, offset=offset)
            playlists = current_user_playlists['items']
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
            # increment
            offset += 50

        # All playlists info into a pandas dataframe
        df = pd.DataFrame(play_lists)

        # Save dataframe into a CSV
        try:
            df.to_csv(csv_filepath, index=False)
            print(f"All Albums dataFrame successfully saved in {csv_filepath}.")
        except IOError:
            print("ERROR: Unable to write to the CSV file.")
        except Exception as e:
            print("An unexpected error occured: {e}")

        return None


    # def fetch_tracks_from_playlist(self):
    #     pass