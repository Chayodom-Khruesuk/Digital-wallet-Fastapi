from typing import Optional
from pydantic import BaseModel, ConfigDict
from sqlmodel import Field, Relationship, SQLModel

from .item_model import DBItem
from .wallet_model import DBWallet


class BaseTransaction(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    wallet_id: int
    balance: float
    description: str | None = None


class CreatedTransaction(BaseTransaction):
    pass


class UpdatedTransaction(BaseTransaction):
    pass


class Transaction(BaseTransaction):
    id: int

class DBTransaction(Transaction, SQLModel, table=True):
    __tablename__ = "transactions"
    id: Optional[int] = Field(default=None, primary_key=True)

    wallet_id: Optional[int] = Field(default=None, foreign_key="wallets.id")
    wallet: Optional[DBWallet] = Relationship(back_populates="transactions")

    item_id: Optional[int] = Field(default=None, foreign_key="items.id")
    item: Optional[DBItem] = Relationship(back_populates="transactions")
    
class TransactionList(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    transactions: list[Transaction]
    page: int
    page_size: int
    size_per_page: int