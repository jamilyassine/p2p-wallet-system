from fastapi import APIRouter

router = APIRouter()


@router.get("/users")
def get_users():
    return {"message": "Not implemented yet"}

@router.post("/users")
def create_user():
    return {"message": "Not implemented yet"}

    

