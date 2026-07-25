"""
Initialize the database schema for local development.

All SQLAlchemy models must be imported before calling create_all()
so they are registered with Base.metadata.
"""

from app.db.session import Base, engine

# Import models so SQLAlchemy registers them with Base.metadata.
from app.models.transfers import Transfer
from app.models.user import User
from app.models.wallet import Wallet


#Base.metadata.create_all(bind=engine)



