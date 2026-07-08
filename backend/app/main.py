from fastapi import FastAPI
from app.api.health import router as health_router
from app.api import users, wallets, transfers
import app.db.init_db

app = FastAPI()

app.include_router(health_router)

app.include_router(users.router)
app.include_router(wallets.router)
app.include_router(transfers.router)









