from app.models.wallet import Wallet
from fastapi import HTTPException


def transfer(db, sender_id: int, receiver_id: int, amount: float):

    if amount <= 0:
        raise HTTPException(
            status_code=400,
            detail="Transfer amount must be greater than zero"
        )

    if sender_id == receiver_id:
        raise HTTPException(
            status_code=400,
            detail="Sender and receiver wallets must be different"
        )


    sender_wallet = (
        db.query(Wallet)
        .filter(Wallet.id == sender_id)
        .first()
    )

    if sender_wallet is None:
        raise HTTPException(
            status_code=404,
            detail="Sender wallet not found"
        )

    receiver_wallet = (
        db.query(Wallet)
        .filter(Wallet.id == receiver_id)
        .first()
    )

    if receiver_wallet is None:
        raise HTTPException(
            status_code=404,
            detail="Receiver wallet not found"
        )

    sender_wallet.balance -= amount
    receiver_wallet.balance += amount

    db.commit()

    return sender_wallet, receiver_wallet