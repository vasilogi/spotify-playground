from dotenv import load_dotenv
from pathlib import Path
import argparse
import time
import os

# Custom modules
from src.spotify_handler import SpotifyAPI

def main():
    # get current workind directory
    cwd = Path.cwd()

    # Load variables from .env file
    load_dotenv()

    # Get Spotify application's credentials
    client_id=os.environ.get('CLIENT_ID')
    client_secret=os.environ.get('CLIENT_SECRET')
    redirect_uri=os.environ.get('REDIRECT_URI')
    scope = "user-library-read"

    spotify = SpotifyAPI(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
    )

    # Authorize Spotify Client
    spotify.connect(scope=scope)

    # Get all albums
    csv_filepath = cwd / "all_albums.csv"
    spotify.fetch_all_albums(csv_filepath=csv_filepath)

if __name__ == '__main__':
    main()