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
parser.add_argument('--playlist_id', required=True, help='The playlist ID')

# Parse arguments
args = parser.parse_args()

# Get playlist ID
playlist_id=args.playlist_id


offset=0
limit=100
tracks = []

# First get the playlist info to know total tracks
try:
    playlist_info = sp.playlist(playlist_id)
    total_tracks = playlist_info['tracks']['total']
    print(f"Fetching {total_tracks} tracks from playlist: {playlist_info['name']}")
    playlist_name = playlist_info['name'].replace(" ", "")
except Exception as e:
    print(f"Error getting playlist information: {e}")

with tqdm(total=total_tracks, desc='Fetching tracks') as pbar:
    # handle limit
    while True:
        try:
            # Get the playlist tracks object
            playlist_tracks = sp.playlist_tracks(playlist_id=playlist_id, limit=limit, offset=offset)
            # Get playlist items
            playlist_items = playlist_tracks['items']
            # Exit if no playlist items exist
            if len(playlist_items) == 0:
                break
            # Process each track
            for item in playlist_items:
                # check if track exists
                if item['track'] is not None:
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
            # Update progress and offset
            offset+=limit
            pbar.update(len(playlist_items))

            # Avoid rate limiting with a small pause
            time.sleep(0.5)
        except Exception as e:
            print(f"Error occured: {e}")
            time.sleep(3)
            continue



if tracks:
    # Save to a CSV file
    df = pd.DataFrame(tracks)
    output_path='playlist_trakcs_' + playlist_name + '.csv'
    df.to_csv(output_path, index=False)
    print(f"Saved albums exported to {output_path}")
else:
    print("No tracks were fetched")