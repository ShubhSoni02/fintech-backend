from fastapi import FastAPI
from . import models
from .database import engine
from .routers import users, auth, transactions

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(transactions.router)

@app.get("/")
def root():
    return {"message" : "Finftech API"}