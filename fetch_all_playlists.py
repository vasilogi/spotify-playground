# Standard Imports
from pathlib import Path
import argparse
import os

# Third-party
from dotenv import load_dotenv

# Custom modules
from src.data_fetcher import DataFetcher
from src.spotify_client import SpotifyClient

def arg_parser():
    """Function to parse arguments from terminal"""
    parser = argparse.ArgumentParser(description='Script to get all stored playlists')
    parser.add_argument("--scope", type=str, dest='app_scope', default='playlist-read-private')
    parser.add_argument(
        "--output-csv-path",
        type=Path,
        dest='output_path',
        default='./all_playlists.csv'
    )
    return parser.parse_args()

def main():
    """Main program"""
    # Load variables from .env file
    load_dotenv()

    # Define arguments
    args = arg_parser()

    # Get Spotify application's credentials
    client_id=os.environ.get('CLIENT_ID')
    client_secret=os.environ.get('CLIENT_SECRET')
    redirect_uri=os.environ.get('REDIRECT_URI')
    scope = args.app_scope

    # Instantiate Spotify Client using a Context Manager
    with SpotifyClient(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope=scope
    ) as client:
        # Instantiate Data Fetcher
        data_fetcher = DataFetcher(client)

        # Get all data
        data_fetcher.fetch_all_playlists(csv_filepath=args.output_path)

if __name__ == '__main__':
    main()
