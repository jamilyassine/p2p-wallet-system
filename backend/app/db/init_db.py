from app.db.session import Base, engine

# Import all models
from app.models.user import User
from app.models.wallet import Wallet
from app.models.transfers import Transfer

Base.metadata.create_all(bind=engine)










