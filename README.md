# spotify-playground

python -m venv .venv

```bash
python .\fetch_all_albums.py --scope "user-library-read" --output-csv-path "./all_albums.csv"
```

scopes

'user-library-read' for fetching all albums
'playlist-read-private' for fetching all playlists
'playlist-read-private' for fetching tracks from playlists