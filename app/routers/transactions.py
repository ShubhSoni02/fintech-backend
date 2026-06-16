from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"]
)

@router.post("/deposit", response_model=schemas.TransactionResponse)
def deposit(deposit : schemas.Deposit, db : Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    current_user.balance+=deposit.amount
    new_transaction = models.Transaction(
        transaction_type = "DEPOSIT",
        amount = deposit.amount,
        sender_id = None,
        receiver_id = current_user.id,
        description = "Account Deposit"
    )
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    db.refresh(current_user)
    return {
        "transaction" : new_transaction,
        "current_balance" : current_user.balance
    }

@router.post("/withdraw", response_model=schemas.TransactionResponse)
def withdraw(withdraw : schemas.Withdraw, db : Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    if current_user.balance < withdraw.amount:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Insufficient balance.")
    current_user.balance-=withdraw.amount
    new_transaction = models.Transaction(
        transaction_type = "WITHDRAW",
        amount = withdraw.amount,
        sender_id = current_user.id,
        receiver_id = None,
        description = "Account withdrawal"
    )
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    db.refresh(current_user)
    return {
        "transaction" : new_transaction,
        "current_balance" : current_user.balance
    }

@router.post("/transfer", response_model=schemas.TransactionResponse)
def transfer(transfer : schemas.Transfer, db : Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    receiver = db.query(models.User).filter(models.User.id==transfer.receiver_id).first()
    if not receiver:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"receiver with id : {transfer.receiver_id} not found.")
    
    if transfer.receiver_id == current_user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= "Cannot transfer to yourself.")
    
    if current_user.balance < transfer.amount:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= "Insufficient balance.")
    
    current_user.balance -= transfer.amount
    receiver.balance += transfer.amount

    new_transaction = models.Transaction(
        transaction_type = "TRANSFER",
        amount = transfer.amount,
        sender_id = current_user.id,
        receiver_id = receiver.id,
        description = transfer.description
    )
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    db.refresh(current_user)
    db.refresh(receiver)
    return {
        "transaction" : new_transaction,
        "current_balance" : current_user.balance
    }

@router.get("/history", response_model=list[schemas.TransactionOut])
def get_history(db : Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    transactions = db.query(models.Transaction).filter(
        (models.Transaction.sender_id == current_user.id) |
        (models.Transaction.receiver_id == current_user.id)
    ).all()
    return transactions

