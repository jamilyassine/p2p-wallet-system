
from sqlalchemy.orm import Session
from datetime import datetime
from app.models.transfers import Transfer, TransferStatus
from app.repositories.transfer_repository import transfer_repository
from app.repositories.wallet_repository import wallet_repository
from app.exceptions import *



def transfer(db : Session, sender_id: int, receiver_id: int, amount: float):

    if amount <= 0:
        '''
        raise HTTPException(
            status_code=400,
            detail="Transfer amount must be greater than zero"
        )
        '''
        raise InvalidTransferAmountException()

    if sender_id == receiver_id:
        '''
        raise HTTPException(
            status_code=400,
            detail="Sender and receiver wallets must be different"
        )
        '''
        raise SelfTransferException()


    sender_wallet = wallet_repository.get_by_user_id(
        db,
        sender_id,
    )

    if sender_wallet is None:
        '''
        raise HTTPException(
            status_code=404,
            detail="Sender wallet not found"
        )
        '''
        raise WalletNotFoundException()

    receiver_wallet = wallet_repository.get_by_user_id(
        db,
        receiver_id,
    )

    if receiver_wallet is None:
        '''
        raise HTTPException(
            status_code=404,
            detail="Receiver wallet not found"
        )
        '''
        raise WalletNotFoundException()

    if sender_wallet.balance < amount:
        '''
        raise HTTPException(
            status_code=400,
            detail="Insufficient balance"
        )
        '''
        raise InsufficientBalanceException()

    sender_wallet.balance -= amount
    receiver_wallet.balance += amount

    transfer = Transfer(
        sender_wallet_id=sender_wallet.id,
        receiver_wallet_id=receiver_wallet.id,
        amount=amount,
        status=TransferStatus.SUCCESS,
        completed_at=datetime.utcnow(),
    )

    transfer_repository.create(
        db,
        transfer,
    )

    return sender_wallet, receiver_wallet


def get_transfers_by_user_id(db: Session, user_id: int):

    wallet = wallet_repository.get_by_user_id(db, user_id)

    
    if wallet is None:
        '''
        raise HTTPException(
            status_code=404,
            detail="Wallet not found"
        )
        '''
        raise WalletNotFoundException()

    return transfer_repository.get_by_wallet(
        db,
        wallet.id,
    )


