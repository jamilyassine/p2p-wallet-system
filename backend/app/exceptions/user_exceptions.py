class UserNotFoundException(Exception):
    """Raised when a user cannot be found."""


class EmailAlreadyExistsException(Exception):
    """Raised when a user with the given email already exists."""