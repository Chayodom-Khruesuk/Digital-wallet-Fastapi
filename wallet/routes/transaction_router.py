from fastapi import APIRouter, HTTPException, Depends

from sqlmodel import select

from ..models.item_model import DBItem

from ..models.transaction_model import CreatedTransaction, DBTransaction, Transaction, TransactionList

from ..models.wallet_model import DBWallet

from typing import Annotated

from .. import models

from sqlmodel.ext.asyncio.session import AsyncSession

router = APIRouter(prefix="/transactions", tags=["Transaction"])

@router.post("/{wallet_id}/{item_id}")
async def create_transaction(
    transaction: CreatedTransaction, 
    wallet_id: int, 
    item_id: int,
    session: Annotated[AsyncSession, Depends(models.get_session)],
) -> Transaction:
    db_wallet = await session.get(DBWallet, wallet_id)
    db_item = await session.get(DBItem, item_id)
    if not db_wallet or not db_item:
        raise HTTPException(status_code=404, detail="Wallet or Item not found")

    balance = db_item.price * transaction.quantity
    if db_wallet.balance < balance:
        raise HTTPException(status_code=400, detail="Insufficient balance")

    db_wallet.balance -= balance
    db_transaction = DBTransaction(**transaction.dict())
    
    session.add(db_wallet)
    session.add(db_transaction)
    await session.commit()
    await session.refresh(db_transaction)

    return Transaction.from_orm(db_transaction)

@router.get("/{transaction_id}")
async def get_transaction(
    transaction_id: int,
    session: Annotated[AsyncSession, Depends(models.get_session)],
) -> Transaction:
    db_transaction = await session.get(DBTransaction, transaction_id)
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return Transaction.from_orm(db_transaction)

@router.get("/wallet/{wallet_id}")
async def get_transactions(
    wallet_id: int,
    session: Annotated[AsyncSession, Depends(models.get_session)],
) -> TransactionList: 
    db_transactions = await session.exec(select(DBTransaction).where(DBTransaction.wallet_id == wallet_id)).all()
    
    return TransactionList(db_transactions)

@router.delete("/{transaction_id}")
async def delete_transaction(
    transaction_id: int,
    session: Annotated[AsyncSession, Depends(models.get_session)],
) -> dict:
    db_transaction = await session.get(DBTransaction, transaction_id)
    await session.delete(db_transaction)
    await session.commit()

    return dict(message="Transaction delete success")