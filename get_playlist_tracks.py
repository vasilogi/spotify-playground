import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
from dotenv import load_dotenv
import os
from pathlib import Path
import argparse
import time
from tqdm import tqdm

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

# Create an ArgumentParser object
parser = argparse.ArgumentParser(
    description="This script takes the playlist ID as an input and generates a list of all tracks"
    )

# Define arguments (required)
parser.add_argument('playlist_id', help='The playlist ID')

# Parse arguments
args = parser.parse_args()

# Get playlist ID
playlist_id=args.playlist_id


offset=0
limit=100
tracks = []

with tqdm(desc='Fetching tracks') as pbar:
    # handle limit
    while True:
        try:
            # Get the playlist tracks object
            playlist_tracks = sp.playlist_tracks(playlist_id=playlist_id, limit=limit, offset=offset)
            # Get playlist items
            playlist_items = playlist_tracks['items']
            # Exit if no playlist items exist
            if len(playlist_tracks) == 0:
                break
            for item in playlist_items:
                track = item['track']
                tracks.append(
                    {
                        'Track ID':track['id'],
                        'Track Name': track['name'],
                        'Track Popularity': track['popularity'],
                        'Track Duration': track['duration_ms'],
                        'Track Album Name': track['album']['name'],
                        'Track Artists': ", ".join(artist['name'] for artist in track['artists'])
                    }
                )
            # Increment
            offset+=limit
            pbar.update(len(playlist_items))
        except Exception as e:
            print(f"Error occured: {e}")
            time.sleep(3)
            continue



# # Save to a CSV file
# df = pd.DataFrame(albums)
# df.to_csv('saved_albums.csv', index=False)

# print("Saved albums exported to 'saved_albums.csv'")