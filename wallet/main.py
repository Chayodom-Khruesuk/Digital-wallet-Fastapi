from fastapi import FastAPI

from sqlmodel import SQLModel

from routes import item_router, merchant_router, wallet_router, transaction_router

from models.database import engine


app = FastAPI()

app.include_router(item_router.router)
app.include_router(merchant_router.router)
app.include_router(wallet_router.router)
app.include_router(transaction_router.router)

#SQLModel.metadata.create_drop(engine)
SQLModel.metadata.create_all(engine)

@app.get("/")
def root():
    return {"message": "Digital Wallet"}
