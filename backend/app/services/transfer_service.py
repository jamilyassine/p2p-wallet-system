from app.models.wallet import Wallet
from fastapi import HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session
from datetime import datetime
from app.models.transfers import Transfer, TransferStatus

def transfer(db : Session, sender_id: int, receiver_id: int, amount: float):

    status=TransferStatus.PENDING

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
        .filter(Wallet.user_id == sender_id)
        .first()
    )

    if sender_wallet is None:
        raise HTTPException(
            status_code=404,
            detail="Sender wallet not found"
        )

    receiver_wallet = (
        db.query(Wallet)
        .filter(Wallet.user_id == receiver_id)
        .first()
    )

    if receiver_wallet is None:
        raise HTTPException(
            status_code=404,
            detail="Receiver wallet not found"
        )

    if sender_wallet.balance < amount:
        raise HTTPException(
            status_code=400,
            detail="Insufficient funds"
        )
    sender_wallet.balance -= amount
    receiver_wallet.balance += amount

    transfer = Transfer(
        sender_wallet_id=sender_wallet.id,
        receiver_wallet_id=receiver_wallet.id,
        amount=amount,
        status=TransferStatus.SUCCESS,
        completed_at=datetime.utcnow(),
    )

    db.add(transfer)

    db.commit()

    transfer.status = TransferStatus.SUCCESS
    transfer.completed_at = datetime.utcnow()

    db.refresh(transfer)

    return sender_wallet, receiver_wallet


def get_transfers_by_user_id(db: Session, user_id: int):

    wallet = (
        db.query(Wallet)
        .filter(Wallet.user_id == user_id)
        .first()
    )

    if wallet is None:
        raise HTTPException(
            status_code=404,
            detail="Wallet not found"
        )

    return (
        db.query(Transfer)
        .filter(
            or_(
                Transfer.sender_wallet_id == wallet.id,
                Transfer.receiver_wallet_id == wallet.id,
            )
        )
        .order_by(Transfer.created_at.desc())
        .all()
    )

