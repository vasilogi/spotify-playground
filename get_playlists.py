import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
from dotenv import load_dotenv
import os
from pathlib import Path

# get current workind directory
cwd = Path.cwd()

# Load variables from .env file
load_dotenv()

# Get Spotify application's credentials
client_id=os.environ.get('CLIENT_ID')
client_secret=os.environ.get('CLIENT_SECRET')
redirect_uri=os.environ.get('REDIRECT_URI')
scope = "playlist-read-private"

# Initialize the Spotify client with OAuth2 using the spotipy library.

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope=scope
))

play_lists = []
offset = 0
# loop over all current user playlists
while True:
    current_user_playlists = sp.current_user_playlists(limit=50, offset=offset)
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
csv_filename = 'current_user_playlists.csv'
csv_filepath = cwd/csv_filename
df.to_csv(csv_filepath, index=False)