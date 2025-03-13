class SpotifyAPIError(Exception):
    """Base exception for Spotify API errors"""

class AuthenticationError(SpotifyAPIError):
    """Raised when authentication fails"""

class InvalidParameterError(SpotifyAPIError):
    """Raised when an invalid parameter is provided"""

class UnexpectedAuthenticationError(SpotifyAPIError):
    """Raised when an unexpected error occurs during authentication"""

class FileWriteError(Exception):
    """Raised when there's an error writing to a file"""

class UnexpectedError(Exception):
    """Raised for any unexpected errors"""
