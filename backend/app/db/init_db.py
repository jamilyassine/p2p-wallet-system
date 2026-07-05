from app.db.session import Base, engine

# Import all models
from app.models.user import User
from app.models.wallet import Wallet

Base.metadata.create_all(bind=engine)

