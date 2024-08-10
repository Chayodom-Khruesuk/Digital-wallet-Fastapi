from fastapi import APIRouter, HTTPException, Depends

from sqlmodel import select

from ..models.item_model import DBItem

from ..models.transaction_model import CreatedTransaction, DBTransaction, Transaction, TransactionList, UpdatedTransaction

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

@router.get("")
async def read_transactions(
    session: Annotated[AsyncSession, Depends(models.get_session)],
    page: int = 1, 
    page_size: int = 10
) -> TransactionList:
    db_transactions = await session.exec(
        select(DBTransaction).offset((page - 1) * page_size).limit(page_size)
    )
    db_transactions = db_transactions.all()
    return TransactionList(
        transactions=db_transactions,
        page=page,
        page_size=page_size,
        size_per_page=len(db_transactions),
    )

@router.get("/{transaction_id}")
async def get_transaction(
    transaction_id: int,
    session: Annotated[AsyncSession, Depends(models.get_session)],
) -> Transaction:
    db_transaction = await session.get(DBTransaction, transaction_id)
    return Transaction.from_orm(db_transaction)

@router.put("/{transaction_id}")
async def update_transaction(
    transaction_id: int, 
    transaction: UpdatedTransaction, 
    session: Annotated[AsyncSession, Depends(models.get_session)]
) -> Transaction:
    db_transaction = await session.get(DBTransaction, transaction_id)
    if db_transaction:
        for key, value in transaction.dict().items():
            setattr(db_transaction, key, value)
        session.add(db_transaction)
        await session.commit()
        await session.refresh(db_transaction)
        return Transaction.from_orm(db_transaction)
    raise HTTPException(status_code=404, detail="Transaction not found")

@router.delete("/{transaction_id}")
async def delete_transaction(
    transaction_id: int,
    session: Annotated[AsyncSession, Depends(models.get_session)],
) -> dict:
    db_transaction = await session.get(DBTransaction, transaction_id)
    await session.delete(db_transaction)
    await session.commit()

    return dict(message="Transaction delete success")