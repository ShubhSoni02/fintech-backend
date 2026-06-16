from .database import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Float, Numeric 
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, nullable=False, primary_key=True)
    phone_num = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    balance = Column(Numeric(10,2), nullable=False, server_default="0")
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default = text('now()'))

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, nullable=False, primary_key=True)
    transaction_type = Column(String, nullable=False)
    amount = Column(Numeric(10,2), nullable=False)
    description = Column(String(255))
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    receiver_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
  