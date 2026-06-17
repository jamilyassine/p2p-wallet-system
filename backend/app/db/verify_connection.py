from sqlalchemy import text

from app.db.session import SessionLocal

db = SessionLocal()

result = db.execute(text("SELECT 1"))

print(result.scalar())

db.close()