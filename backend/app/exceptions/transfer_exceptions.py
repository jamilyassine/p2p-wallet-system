class TransferNotFoundException(Exception):
    """Raised when a transfer cannot be found."""


class InsufficientBalanceException(Exception):
    """Raised when a wallet has insufficient funds."""


class InvalidTransferAmountException(Exception):
    """Raised when the transfer amount is less than or equal to zero."""


class SelfTransferException(Exception):
    """Raised when the sender and receiver are the same user."""