from sqlalchemy import Column, Integer, String

from backend1.db.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    fullname = Column(String(50), unique=True)
    email = Column(String(50), unique=True)
    password = Column(String(50))
