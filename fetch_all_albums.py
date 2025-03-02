from dotenv import load_dotenv
from pathlib import Path
import argparse
import time
import os

# Custom modules
from src.data_fetcher import DataFetcher
from src.spotify_client import SpotifyClient

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

    # Instantiate Spotify Client
    spotify_client = SpotifyClient(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope=scope
    )

    # Authorize Spotify Client
    client = spotify_client.create_spotify_client()

    # Instantiate Data Fetcher
    data_fetcher = DataFetcher(client)

    # Get all albums
    csv_filepath = cwd / "all_albums.csv"
    data_fetcher.fetch_all_albums(csv_filepath=csv_filepath)

if __name__ == '__main__':
    main()