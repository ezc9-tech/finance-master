import os
from datetime import datetime, date
from typing import List, Optional
from decimal import Decimal

from sqlalchemy import String, DateTime, Date, Numeric, Boolean, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from sqlalchemy_utils import EncryptedType
from sqlalchemy_utils.types.encrypted.encrypted_type import FernetEngine
from backend.db.db import engine

SECRET_KEY = os.environ.get("SECRET_KEY")

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    
    # Basic user information
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(300), nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(String(100), nullable=False)
    connection_status: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    
    # Timestamps for record keeping
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, onupdate=func.now(), nullable=True)

    # Relationships
    connections: Mapped[List["Connection"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    accounts: Mapped[List["Account"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    categories: Mapped[List["Category"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    budgets: Mapped[List["Budget"]] = relationship(back_populates="user", cascade="all, delete-orphan")


class Connection(Base):
    __tablename__ = "connections"
    
    connection_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    
    # Encrypt the SimpleFIN access URL because it acts as a persistent credential
    simplefin_access_url: Mapped[str] = mapped_column(
        EncryptedType(String(255), SECRET_KEY, FernetEngine), 
        nullable=False, 
        unique=True
    )
    
    user: Mapped["User"] = relationship(back_populates="connections")


class Account(Base):
    __tablename__ = "accounts"
    
    account_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    
    # SimpleFIN's string ID (essential for syncing so you don't create duplicates)
    simplefin_account_id: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    
    org_name: Mapped[str] = mapped_column(String(100), nullable=False) # e.g., "Chase" or "Bank of America"
    account_name: Mapped[str] = mapped_column(String(100), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="USD")
    
    # Use Numeric for currency to avoid floating point math errors
    current_balance: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    available_balance: Mapped[Optional[Decimal]] = mapped_column(Numeric(12, 2), nullable=True)
    
    last_synced_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    # Relationships
    user: Mapped["User"] = relationship(back_populates="accounts")
    transactions: Mapped[List["Transaction"]] = relationship(back_populates="account", cascade="all, delete-orphan")
    balance_history: Mapped[List["BalanceHistory"]] = relationship(back_populates="account", cascade="all, delete-orphan")


class BalanceHistory(Base):
    __tablename__ = "balance_history"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.account_id"))
    
    balance: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False)

    # Relationships
    account: Mapped["Account"] = relationship(back_populates="balance_history")


class Category(Base):
    __tablename__ = "categories"
    
    category_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True) 
    
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    type: Mapped[str] = mapped_column(String(20), nullable=False) # 'income', 'expense', 'transfer'

    # Relationships
    user: Mapped[Optional["User"]] = relationship(back_populates="categories")
    transactions: Mapped[List["Transaction"]] = relationship(back_populates="category")
    budgets: Mapped[List["Budget"]] = relationship(back_populates="category")


class Transaction(Base):
    __tablename__ = "transactions"
    
    transaction_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.account_id"))
    category_id: Mapped[Optional[int]] = mapped_column(ForeignKey("categories.category_id"), nullable=True)
    
    # SimpleFIN's string UUID for the transaction (prevents duplicates on re-sync)
    simplefin_transaction_id: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    
    date_posted: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    
    raw_description: Mapped[str] = mapped_column(String(255), nullable=False) 
    payee: Mapped[Optional[str]] = mapped_column(String(100), nullable=True) 
    
    is_pending: Mapped[bool] = mapped_column(Boolean, default=False)

    # Relationships
    account: Mapped["Account"] = relationship(back_populates="transactions")
    category: Mapped[Optional["Category"]] = relationship(back_populates="transactions")


class Budget(Base):
    __tablename__ = "budgets"
    
    budget_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.category_id"))
    
    amount_limit: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    period: Mapped[str] = mapped_column(String(20), default="monthly") # 'weekly', 'monthly', 'yearly'

    # Relationships
    user: Mapped["User"] = relationship(back_populates="budgets")
    category: Mapped["Category"] = relationship(back_populates="budgets")
    

Base.metadata.create_all(engine)