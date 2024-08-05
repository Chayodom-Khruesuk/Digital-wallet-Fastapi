from fastapi import APIRouter, HTTPException

from sqlmodel import Session, select

from models import engine

from models.item_models import DBItem
from models.transaction_model import CreatedTransaction, DBTransaction, Transaction, TransactionList
from models.wallet_model import DBWallet

router = APIRouter(prefix="/transactions", tags=["transaction"])

@router.post("/{wallet_id}/{item_id}")
async def create_transaction(
    transaction: CreatedTransaction, wallet_id: int, item_id: int
) -> Transaction:
    data = transaction.dict()
    db_transaction = DBTransaction(**data)
    db_transaction.wallet_id = wallet_id
    db_transaction.item_id = item_id

    with Session(engine) as session:
        db_wallet = session.get(DBWallet, wallet_id)
        db_item = session.get(DBItem, item_id)
        if db_wallet is None or db_item is None:
            raise HTTPException(status_code=404, detail="Item or Wallet not found")

        balance = db_item.price * db_transaction.quantity
        if db_wallet.balance < balance:
            raise HTTPException(status_code=400, detail="Insufficient balance")
        db_wallet.balance -= balance
        db_wallet.sqlmodel_update(db_wallet.dict())

        db_transaction.balance = balance

        session.add(db_transaction)
        session.commit()
        session.refresh(db_transaction)

    return Transaction.from_orm(db_transaction)


@router.get("/{transaction_id}")
async def get_transaction(transaction_id: int) -> Transaction:
    with Session(engine) as session:
        db_transaction = session.get(DBTransaction, transaction_id)
        if db_transaction is None:
            raise HTTPException(status_code=404, detail="Item not found")

        return Transaction.from_orm(db_transaction)


@router.get("/{wallet_id}")
async def get_transactions(wallet_id: int) -> TransactionList:
    with Session(engine) as session:
        db_transactions = session.exec(
            select(DBTransaction).where(DBTransaction.wallet_id == wallet_id)
        ).all()

    return TransactionList(
        transactions=db_transactions,
        page=1,
        page_size=len(db_transactions),
        size_per_page=len(db_transactions),
    )


@router.delete("/{transaction_id}")
async def delete_transaction(transaction_id: int) -> dict:
    with Session(engine) as session:
        db_transaction = session.get(DBTransaction, transaction_id)
        if db_transaction is None:
            raise HTTPException(status_code=404, detail="Item not found")
        session.delete(db_transaction)
        session.commit()

    return dict(message="Transaction deleted successfully")