from pathlib import Path

ROOT_DIRECTORY = Path(__file__).resolve().parent
DOWNLOADS_DIRECTORY = 'downloads'
ABS_DOWNLOADS_PATH = str(ROOT_DIRECTORY / DOWNLOADS_DIRECTORY)

# HTTP Response Codes
REQUEST_TIMEOUT = 408
UNAUTHORIZED = 401
NOT_FOUND = 404
BAD_REQUEST = 400
INTERNAL_SERVER_ERROR = 500
