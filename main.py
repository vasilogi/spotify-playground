import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd

# Replace these with your Spotify application's credentials
CLIENT_ID = "daa86738250042fcbdaff5a421340241"
CLIENT_SECRET = "e955ae0c274d475e82837fe98ddfcb60"
# For local testing, you can use a loopback address like:
REDIRECT_URI = "http://127.0.0.1:8888/callback"
SCOPE = "user-library-read"

# Initialize the Spotify client with OAuth2 using the spotipy library.
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               scope=SCOPE))

# Fetch all saved albums
albums = []
offset = 0
while True:
    results = sp.current_user_saved_albums(limit=50, offset=offset)
    if not results['items']:
        break
    for item in results['items']:
        album = item['album']
        albums.append({
            'Album Name': album['name'],
            'Artists': ", ".join(artist['name'] for artist in album['artists']),
            'Release Date': album['release_date'],
            'Popularity': album['popularity'],
            'Image URL': album['images'][0]['url']
        })
    offset += 50

# Save to a CSV file
df = pd.DataFrame(albums)
df.to_csv('saved_albums.csv', index=False)

print("Saved albums exported to 'saved_albums.csv'")