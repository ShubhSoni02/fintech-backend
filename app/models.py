from .database import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Numeric
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    phone_num = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    balance = Column(Numeric(10, 2), nullable=False, server_default="0")
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))

    sent_transactions = relationship("Transaction", foreign_keys="Transaction.sender_id", back_populates="sender")

    received_transactions = relationship("Transaction", foreign_keys="Transaction.receiver_id", back_populates="receiver")


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, nullable=False)
    transaction_type = Column(String, nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    description = Column(String(255))
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    receiver_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))

    sender = relationship("User", foreign_keys=[sender_id], back_populates="sent_transactions")

    receiver = relationship("User", foreign_keys=[receiver_id], back_populates="received_transactions")