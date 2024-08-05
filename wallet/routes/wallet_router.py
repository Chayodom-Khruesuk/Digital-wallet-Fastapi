from fastapi import APIRouter, HTTPException

from sqlalchemy import Engine

from sqlmodel import Session

from models.wallet_model import CreatedWallet, DBWallet, UpdatedWallet, Wallet

from models.database import engine

router = APIRouter()


@router.post("/wallet/{merchant_id}", tags=["wallet"])
async def create_wallet(wallet: CreatedWallet, merchant_id: int) -> Wallet:
    data = wallet.model_dumpt()
    db_wallet = DBWallet(**data)
    db_wallet.merchant_id = merchant_id
    with Session(Engine) as db:
        db.add(db_wallet)
        db.commit()
        db.refresh(db_wallet)
    return Wallet.model_validate(db_wallet)

@router.get("/wallet/{wallet_id}", tags=["wallet"])
async def get_wallet(wallet_id: int) -> Wallet:
    with Session(engine) as db:
        db_wallet = db.get(DBWallet, wallet_id)
        if db_wallet is None:
            raise HTTPException(status_code=404, detail="Item not found")
        return Wallet.model_validate(db_wallet)
    
@router.put("/wallet/{wallet_id}", tags=["wallet"])
async def update_wallet(wallet_id: int, wallet: UpdatedWallet) -> Wallet:
    with Session(engine) as db:
        db_wallet = db.get(DBWallet, wallet_id)
        if db_wallet is None:
            raise HTTPException(status_code=404, detail="Item not found")
        for key, value in wallet.model_dump().items():
            setattr(db_wallet, key, value)
        db.add(db_wallet)
        db.commit()
        db.refresh(db_wallet)
    return Wallet.model_validate(db_wallet)

@router.delete("/wallet/{wallet_id}", tags=["wallet"])
async def delete_wallet(wallet_id: int) -> dict:
    with Session(engine) as db:
        db_wallet = db.get(DBWallet, wallet_id)
        if db_wallet is None:
            raise HTTPException(status_code=404, detail="Item not found")
        db.delete(db_wallet)
        db.commit()
    return dict(message="Wallet deleted successfully")