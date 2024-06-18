class CarmenAPIConfigError(Exception):
    """
    Exception raised when the provided options for TransportAPIClient are invalid.

    Args:
        message (str): The error message.

    Attributes:
        name (str): The name of the exception.
    """
    def __init__(self, message):
        super().__init__(message)
        self.name = "CarmenAPIConfigError"

class InvalidImageError(Exception):
    """
    Exception raised when the provided image is invalid.

    Args:
        message (str): The error message.

    Attributes:
        name (str): The name of the exception.
    """
    def __init__(self, message):
        super().__init__(message)
        self.name = "InvalidImageError"

class CarmenAPIError(Exception):
    """
    Exception raised when an API call fails after the configured number of retries.

    Args:
        message (str): The error message.

    Attributes:
        name (str): The name of the exception.
    """
    def __init__(self, message):
        super().__init__(message)
        self.name = "CarmenAPIError"
