from fastapi import APIRouter

router = APIRouter()

@router.get("/wallets")
def get_wallets():
    return {"message": "Not implemented yet"}

    