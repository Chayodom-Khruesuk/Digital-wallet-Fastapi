from fastapi import APIRouter, HTTPException, Depends

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
    db_wallet = DBWallet(**wallet.dict())
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
    db_wallet = await session.get(DBWallet, wallet_id)
    db_wallet.sqlmodel_update(**wallet.dict())
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