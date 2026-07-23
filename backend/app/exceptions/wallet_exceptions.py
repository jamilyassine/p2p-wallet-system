class WalletNotFoundException(Exception):
    """Raised when a wallet cannot be found."""


class WalletAlreadyExistsException(Exception):
    """Raised when a wallet already exists for the given user."""