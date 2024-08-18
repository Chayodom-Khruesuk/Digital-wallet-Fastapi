from fastapi import APIRouter, HTTPException, Depends

from wallet.models.merchant_model import DBMerchant
from wallet.models.user_model import DBUser

from ..models.wallet_model import CreatedWallet, DBWallet, UpdatedWallet, Wallet

from typing import Annotated

from .. import models

from sqlmodel.ext.asyncio.session import AsyncSession

router = APIRouter(prefix="/wallets", tags=["Wallet"])


@router.post("/{merchant_id}")
async def create_wallet(
    wallet: CreatedWallet,
    merchant_id: int,
    session: Annotated[AsyncSession, Depends(models.get_session)],
) -> Wallet:
    data = wallet.dict()
    db_wallet = DBWallet(**data)
    db_wallet.merchant_id = merchant_id

    db_merchant = await session.get(DBMerchant, merchant_id)
    db_wallet.name = db_merchant.name

    session.add(db_wallet)
    await session.commit()
    await session.refresh(db_wallet)

    return Wallet.from_orm(db_wallet)

@router.post("/create_user_wallet/{user_id}")
async def create_user_wallet(
    wallet: CreatedWallet,
    user_id: int,
    session: Annotated[AsyncSession, Depends(models.get_session)],
) -> Wallet:
    data = wallet.dict()
    db_wallet = DBWallet(**data)
    session.add(db_wallet)
    await session.commit()
    await session.refresh(db_wallet)
    
    return Wallet.from_orm(db_wallet)

@router.get("/{wallet_id}")
async def get_wallet(
    wallet_id: int,
    session: Annotated[AsyncSession, Depends(models.get_session)],
) -> Wallet:
    db_wallet = await session.get(DBWallet, wallet_id)
    if db_wallet is None:
        raise HTTPException(status_code=404, detail="Wallet not found")
    
    return Wallet.from_orm(db_wallet)

@router.put("/{wallet_id}")
async def update_wallet(
    wallet_id: int, 
    wallet: UpdatedWallet,
    session: Annotated[AsyncSession, Depends(models.get_session)],
) -> Wallet:
    data = wallet.dict()
    db_wallet = await session.get(DBWallet, wallet_id)
    db_wallet.sqlmodel_update(data)
    session.add(db_wallet)
    await session.commit()
    await session.refresh(db_wallet)

    return Wallet.from_orm(db_wallet)

@router.delete("/{wallet_id}")
async def delete_wallet(
    wallet_id: int,
    session: Annotated[AsyncSession, Depends(models.get_session)],
) -> dict:
    db_wallet = await session.get(session, wallet_id)
    await session.delete(db_wallet)
    await session.commit()
    return dict(message="Wallet delete success")