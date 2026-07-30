from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import app.db.init_db

from app.api.health import router as health_router
from app.api.transfers import router as transfers_router
from app.api.users import router as users_router
from app.api.wallets import router as wallets_router
from app.handlers.exception_handlers import register_exception_handlers
from app.api.ledger import router as ledger_router


app = FastAPI()

register_exception_handlers(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(users_router)
app.include_router(wallets_router)
app.include_router(transfers_router)
app.include_router(ledger_router)








