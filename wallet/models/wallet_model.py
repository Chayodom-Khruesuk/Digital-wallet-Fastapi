from typing import Optional, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict

from sqlmodel import Field, SQLModel, Relationship

from models.merchant_model import DBMerchant

class BaseWallet(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    balance: float = 0.0
    

class CreatedWallet(BaseWallet):
    pass

class UpdatedWallet(BaseWallet):
    pass

class Wallet(BaseWallet):
    id: int

class DBWallet(Wallet, SQLModel, table=True):
    __tablename__ = "wallets"
    id: Optional[int] = Field(default=None, primary_key=True)

    merchant_id: Optional[int] = Field(default=None, foreign_key="dbmerchant.id")
    merchant: Optional[DBMerchant] = Relationship(back_populates="wallet")

class WalletList(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    Wallets: list[Wallet]
    page: int
    page_size: int
    size_per_page: int