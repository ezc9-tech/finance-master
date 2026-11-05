import os
from datetime import datetime
from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from backend.db.db import engine
from sqlalchemy_utils import EncryptedType
from sqlalchemy_utils.types.encrypted.encrypted_type import FernetEngine

SECRET_KEY = os.environ.get("SECRET_KEY")

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    
    #Basic user information
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(300), nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(String(100), nullable=False)
    
    # This is all for simplefin integration
    access_url: Mapped[str | None] = mapped_column(
        EncryptedType(String(255), SECRET_KEY, FernetEngine, 'utf-8'), 
        unique=True, 
        nullable=True
    )
    connection_status: Mapped[str | None] = mapped_column(String(50), nullable=True)
    last_sync_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    
    # Timestamps for record keeping
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime | None] = mapped_column(DateTime, onupdate=func.now(), nullable=True)

Base.metadata.create_all(engine)