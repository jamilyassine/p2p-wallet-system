from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.exceptions import (
    EmailAlreadyExistsException,
    InsufficientBalanceException,
    InvalidTransferAmountException,
    SelfTransferException,
    TransferNotFoundException,
    UserNotFoundException,
    WalletAlreadyExistsException,
    WalletNotFoundException,
)


def register_exception_handlers(app: FastAPI) -> None:

    @app.exception_handler(UserNotFoundException)
    async def user_not_found_handler(
        request: Request,
        exc: UserNotFoundException,
    ):
        return JSONResponse(
            status_code=404,
            content={"error": "User not found"},
        )

    @app.exception_handler(WalletNotFoundException)
    async def wallet_not_found_handler(
        request: Request,
        exc: WalletNotFoundException,
    ):
        return JSONResponse(
            status_code=404,
            content={"error": "Wallet not found"},
        )

    @app.exception_handler(WalletAlreadyExistsException)
    async def wallet_already_exists_handler(
        request: Request,
        exc: WalletAlreadyExistsException,
    ):
        return JSONResponse(
            status_code=409,
            content={"error": "Wallet already exists"},
        )

    @app.exception_handler(TransferNotFoundException)
    async def transfer_not_found_handler(
        request: Request,
        exc: TransferNotFoundException,
    ):
        return JSONResponse(
            status_code=404,
            content={"error": "Transfer not found"},
        )

    @app.exception_handler(EmailAlreadyExistsException)
    async def email_exists_handler(
        request: Request,
        exc: EmailAlreadyExistsException,
    ):
        return JSONResponse(
            status_code=409,
            content={"error": "Email already exists"},
        )

    @app.exception_handler(InsufficientBalanceException)
    async def insufficient_balance_handler(
        request: Request,
        exc: InsufficientBalanceException,
    ):
        return JSONResponse(
            status_code=400,
            content={"error": "Insufficient balance"},
        )

    @app.exception_handler(InvalidTransferAmountException)
    async def invalid_amount_handler(
        request: Request,
        exc: InvalidTransferAmountException,
    ):
        return JSONResponse(
            status_code=400,
            content={"error": "Transfer amount must be positive"},
        )

    @app.exception_handler(SelfTransferException)
    async def self_transfer_handler(
        request: Request,
        exc: SelfTransferException,
    ):
        return JSONResponse(
            status_code=400,
            content={"error": "Cannot transfer to yourself"},
        )