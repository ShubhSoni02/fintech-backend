from fastapi import APIRouter
from .. import models, schemas, utils, oauth2
from sqlalchemy.orm import Session
from fastapi import FastAPI, Response, status, HTTPException, Depends
from ..database import get_db

router = APIRouter(
    prefix='/users',
    tags=['Users']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user : schemas.UserCreate, db : Session = Depends(get_db)):

    hashed_password = utils.Hash(user.password)
    user.password = hashed_password

    existing_user = db.query(models.User).filter(
        (models.User.email == user.email) |
        (models.User.phone_num == user.phone_num)
    ).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email or phone no. already registered.")
    
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.UserOut)
def get_user(id : int, db : Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    if current_user.id != id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized.")
    
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id : {id} not found.")
    return user

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id : int, db : Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    if current_user.id != id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized.")
    user_query =db.query(models.User).filter(models.User.id == id) 
    user = user_query.first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"User with id : {id} not found.")

    transaction = db.query(models.Transaction).filter(
        (models.Transaction.sender_id == current_user.id) |
        (models.Transaction.receiver_id == current_user.id)
    ).first()

    if transaction:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= "User has a transaction history and cannot be deleted.")

    user_query.delete(synchronize_session = False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

