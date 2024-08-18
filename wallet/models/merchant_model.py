from typing import Optional, TYPE_CHECKING
from pydantic import BaseModel, ConfigDict
from sqlmodel import Field, Relationship, SQLModel

from . import user_model

class BaseMerchant(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str

class CreatedMerchant(BaseMerchant):
    pass

class UpdatedMerchant(BaseMerchant):
    pass

class Merchant(BaseMerchant):
    id: int

class DBMerchant(BaseMerchant, SQLModel, table=True):
    __tablename__ = "merchants"
    id: Optional[int] = Field(default=None, primary_key=True)

    items: list["DBItem"] = Relationship(back_populates="merchant", cascade_delete=True)

    wallet: Optional["DBWallet"] = Relationship(back_populates="merchant", cascade_delete=True)

    user_id: Optional[int] = Field(default=None, foreign_key="users.id")
    user: user_model.DBUser | None = Relationship()


class MerchantList(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    merchants: list[Merchant]
    page: int
    page_size: int
    size_per_page: int

if TYPE_CHECKING:
    from .item_model import DBItem
    from .wallet_model import DBWallet