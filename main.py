# Standard Imports
import os

# Third-party
from dotenv import load_dotenv
import typer
from rich import print

# Custom modules
from src.data_fetcher import DataFetcher
from src.spotify_wrapper import SpotifyClient

# TODO: add markdown helper
app = typer.Typer(
    no_args_is_help=True,
    help="A custom Spotify Command Line Interface"
)

@app.command()
def fetch_albums(output_path: str = './all_albums.csv', pagination_limit: int = 50):
    """
    Fetch all saved albums for the current user and save them to a CSV file.
    """
    # Load variables from .env file
    load_dotenv()

    # Get Spotify application's credentials
    client_id=os.environ.get('CLIENT_ID')
    client_secret=os.environ.get('CLIENT_SECRET')
    redirect_uri=os.environ.get('REDIRECT_URI')
    app_scope = os.environ.get('SCOPE')

    # Instantiate Spotify Client using a Context Manager
    with SpotifyClient(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope=app_scope
    ) as client:
        # Instantiate Data Fetcher
        data_fetcher = DataFetcher(client)

        # Get all data
        data_fetcher.fetch_all_albums(
            csv_filepath=output_path,
            pagination_limit=pagination_limit
        )

@app.command()
def fetch_playlists(output_path: str = './all_playlists.csv', pagination_limit: int = 50):
    """
    Fetch all saved playlists for the current user and save them to a CSV file.
    """
    # Load variables from .env file
    load_dotenv()

    # Get Spotify application's credentials
    client_id=os.environ.get('CLIENT_ID')
    client_secret=os.environ.get('CLIENT_SECRET')
    redirect_uri=os.environ.get('REDIRECT_URI')
    app_scope = os.environ.get('SCOPE')

    # Instantiate Spotify Client using a Context Manager
    with SpotifyClient(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope=app_scope
    ) as client:
        # Instantiate Data Fetcher
        data_fetcher = DataFetcher(client)

        # Get all data
        data_fetcher.fetch_all_playlists(
            csv_filepath=output_path,
            pagination_limit=pagination_limit
        )

@app.command()
def fetch_playlist_tracks(playlist_id: str, output_path: str, pagination_limit: int = 50):
    """
    Fetch all tracks from a chosen playlist and save them to a CSV file.
    """
    # Load variables from .env file
    load_dotenv()

    # Get Spotify application's credentials
    client_id=os.environ.get('CLIENT_ID')
    client_secret=os.environ.get('CLIENT_SECRET')
    redirect_uri=os.environ.get('REDIRECT_URI')
    app_scope = os.environ.get('SCOPE')

    # Instantiate Spotify Client using a Context Manager
    with SpotifyClient(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope=app_scope
    ) as client:
        # Instantiate Data Fetcher
        data_fetcher = DataFetcher(client)

        data_fetcher.fetch_tracks_from_playlist(
            playlist_id=playlist_id,
            csv_filepath=output_path,
            pagination_limit=pagination_limit
        )

if __name__ == '__main__':
    app()
