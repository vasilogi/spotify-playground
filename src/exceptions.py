class SpotifyAPIError(Exception):
    """Base exception for Spotify API errors"""
    pass

class AuthenticationError(SpotifyAPIError):
    """Raised when authentication fails"""
    pass

class InvalidParameterError(SpotifyAPIError):
    """Raised when an invalid parameter is provided"""
    pass

class UnexpectedAuthenticationError(SpotifyAPIError):
    """Raised when an unexpected error occurs during authentication"""
    pass

class FileWriteError(Exception):
    """Raised when there's an error writing to a file"""
    pass

class UnexpectedError(Exception):
    """Raised for any unexpected errors"""
    pass
