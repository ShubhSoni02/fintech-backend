from fastapi import FastAPI
from . import models
from .database import engine
from .routers import users, auth, transactions
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = False,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(transactions.router)

@app.get("/")
def root():
    return {"message" : "Finftech API"}