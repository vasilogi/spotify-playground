# Spotify CLI Data Exporter

A command-line interface tool for exporting your Spotify library data to CSV format. This tool allows you to easily extract your saved albums, playlists, and track details for analysis or backup purposes.

![Spotify CLI](https://img.shields.io/badge/Spotify-CLI-1DB954?style=for-the-badge&logo=spotify&l/img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python&logoColor=whiteelds.io/badge/License-MIT-yellow?stures

- Export all saved albums to CSV
- Export all playlists to CSV
- Export tracks from a specific playlist to CSV
- Configurable pagination limits
- Custom output file paths

## 🛠️ Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/vasilogi/spotify-playground.git
   cd spotify-playground
   ```

2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up your Spotify API credentials:
   - Create an application in the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/)
   - Get your Client ID and Client Secret
   - Add a redirect URI (e.g., http://localhost:8888/callback)
   - Create a `.env` file in the project root with the following content:
     ```
     CLIENT_ID=your_client_id
     CLIENT_SECRET=your_client_secret
     REDIRECT_URI=your_redirect_uri
     SCOPE=user-library-read playlist-read-private playlist-read-collaborative
     ```

## 🚀 Usage

The CLI provides several commands for different export operations:

### Export All Saved Albums

```bash
python main.py fetch-albums --output-path ./my_albums.csv --pagination-limit 50
```

### Export All Playlists

```bash
python main.py fetch-playlists --output-path ./my_playlists.csv
```

### Export Tracks from a Specific Playlist

```bash
python main.py fetch-playlist-tracks --playlist-id 37i9dQZF1DX4sWSpwq3LiO --output-path ./discover_weekly_tracks.csv
```

### Help

To see all available commands and options:

```bash
python main.py --help
```

For help on a specific command:

```bash
python main.py fetch-albums --help
```

## 📋 Command Options

| Command | Option | Description | Default |
|---------|--------|-------------|---------|
| `fetch-albums` | `--output-path` | Path where the CSV file will be saved | `./all_albums.csv` |
| `fetch-albums` | `--pagination-limit` | Number of items to fetch per API request | `50` |
| `fetch-playlists` | `--output-path` | Path where the CSV file will be saved | `./all_playlists.csv` |
| `fetch-playlists` | `--pagination-limit` | Number of items to fetch per API request | `50` |
| `fetch-playlist-tracks` | `--playlist-id` | Spotify ID of the playlist | Required |
| `fetch-playlist-tracks` | `--output-path` | Path where the CSV file will be saved | Required |
| `fetch-playlist-tracks` | `--pagination-limit` | Number of items to fetch per API request | `50` |

## 🏗️ Project Structure

```
spotify-playground/
├── main.py             # Main CLI application
├── requirements.txt    # Project dependencies
├── .env                # Environment variables (create this file)
├── src/
│   ├── __init__.py
│   ├── data_fetcher.py # Handles data retrieval and CSV export
│   ├── exceptions.py   # Custom exceptions
│   └── spotify_wrapper.py # Wrapper for Spotify API client
```

## 🔄 Authentication Flow

On first run, the application will:
1. Open your default web browser to authenticate with Spotify
2. Ask you to authorize the application
3. Redirect you to your specified redirect URI
4. Cache your credentials locally for future use

## 🛡️ License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 To-Do

- [ ] Add support for exporting track audio features
- [ ] Implement data visualization capabilities
- [ ] Add more export format options (JSON, Excel)
- [ ] Create a more modular code structure
- [ ] Improve error handling and user feedback