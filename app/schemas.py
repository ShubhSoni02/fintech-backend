from datetime import datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    full_name : str
    email : EmailStr
    phone_num : str = Field(
        pattern=r"^\d{10}$",
        description="Phone Number must be exactly 10 digits"
    )
    password : str

class UserOut(BaseModel):
    id : int
    full_name : str
    email : EmailStr
    phone_num : str
    balance : Decimal
    created_at : datetime
    class Config: 
        orm_mode = True

class UserLogin(BaseModel):
    email : EmailStr
    password : str

class Transfer(BaseModel):
    receiver_id : int
    amount : Decimal
    description : Optional[str] = None

class TransactionOut(BaseModel):
    id : int
    transaction_type : str
    amount : Decimal
    description : Optional[str] = None
    sender_id : Optional[int] = None
    receiver_id : Optional[int] = None
    created_at : datetime
    class Config:
        orm_mode = True

class TransactionResponse(BaseModel):
    transaction : TransactionOut
    current_balance : Decimal

class Deposit(BaseModel):
    amount : Decimal = Field(gt=0)

class Withdraw(BaseModel):
    amount : Decimal = Field(gt=0)
    
class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    id : Optional[int] = None
