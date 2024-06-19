# Plex Assets Manager

A Python project for managing and organizing Plex media library.

## Features

- Reorganize movie folders
- Rename movie files
- Download trailers
- Download subtitles

## Installation

To install the package, you can use `pip`:

```bash
pip install plex-extension
```

## Usage

You can use the package by running the main script with the desired function:

```bash
python -m plex_extension.main <function_id> [options]
```

### Functions

1. **Reorganize folders**: Reorganize movie folders.
2. **Rename movie files**: Rename movie files to a standard format.
3. **Download trailers**: Download trailers for movies.
4. **Download subtitles**: Download subtitles for movies.

### Example

To reorganize folders, you would run:

```bash
python -m plex_extension.main 1
```

## Command Line Options

- `-q`, `--quiet`: Quiet Mode: no logging of intermediate steps.
- `-l`, `--log`: Writes logs to a log file. Default is to show on console.
- `-t`, `--token`: Plex API token. If not specified, the value is taken from the conf file.
- `-u`, `--url`: Plex URL. If not specified, the value is taken from the conf file.
- `-m`, `--movielib`: Name of the Films library in Plex. If not specified, the value is taken from the conf file.

## Configuration

Configuration settings are managed in the `conf.py` file. Ensure you update this file with your specific settings.

```python
# conf.py
PLEX_API_TOKEN = 'your_plex_api_token_here'
OPENSUBTITLES_API_KEY = 'your_opensubtitles_api_key_here'
PLEX_URL = "http://127.0.0.1:32400"
MOVIES_LIBRARY = 'Movies'
LOG = True
QUIET = False
MIN_VIEWS = 10000
MAX_FILESIZE_MB = 100
MIN_FILESIZE_MB = 1
MAX_SLEEP_DURATION = 15
MAX_DAILY_SUB_DOWNLOADS = 20
SUB_DOWNLOAD_TRACK_FILE = "sub_download_tracker.txt"
```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License.