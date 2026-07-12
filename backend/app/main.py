from fastapi import FastAPI
from app.api.health import router as health_router
from app.api import users, wallets, transfers
import app.db.init_db
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)

app.include_router(users.router)
app.include_router(wallets.router)
app.include_router(transfers.router)









