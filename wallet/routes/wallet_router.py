from fastapi import APIRouter, HTTPException

from sqlmodel import Session

from models import engine

from models.wallet_model import CreatedWallet, DBWallet, UpdatedWallet, Wallet


router = APIRouter(prefix="/wallets", tags=["wallet"])


@router.post("/{merchant_id}")
async def create_wallet(wallet: CreatedWallet, merchant_id: int) -> Wallet:
    data = wallet.dict()
    db_wallet = DBWallet(**data)
    db_wallet.merchant_id = merchant_id
    with Session(engine) as session:
        session.add(db_wallet)
        session.commit()
        session.refresh(db_wallet)

    return Wallet.from_orm(db_wallet)

@router.get("/{wallet_id}")
async def get_wallet(wallet_id: int) -> Wallet:
    with Session(engine) as session:
        db_wallet = session.get(DBWallet, wallet_id)
        if db_wallet is None:
            raise HTTPException(status_code=404, detail="Item not found")
        return Wallet.from_orm(db_wallet)
    
@router.put("/{wallet_id}")
async def update_wallet(wallet_id: int, wallet: UpdatedWallet) -> Wallet:
    with Session(engine) as session:
        db_wallet = session.get(DBWallet, wallet_id)
        if db_wallet is None:
            raise HTTPException(status_code=404, detail="Item not found")
        for key, value in wallet.dict().items():
            setattr(db_wallet, key, value)

        session.add(db_wallet)
        session.commit()
        session.refresh(db_wallet)

    return Wallet.from_orm(db_wallet)

@router.delete("/{wallet_id}")
async def delete_wallet(wallet_id: int) -> dict:
    with Session(engine) as session:
        db_wallet = session.get(DBWallet, wallet_id)
        if db_wallet is None:
            raise HTTPException(status_code=404, detail="Item not found")
        session.delete(db_wallet)
        session.commit()

    return dict(message="Wallet deleted successfully")