from typing import Optional

from pydantic import BaseModel, ConfigDict

from sqlmodel import Field, Relationship

from models.merchant_model import Merchant

class BaseItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    description: str | None = None
    price: float = 0.12
    tax: float | None = None

class CreatedItem(BaseItem):
    pass

class UpdatedItem(BaseItem):
    pass

class Item(BaseItem):
    id: int

class DBItem(BaseItem):
    id: int = Field(default=None, primary_key=True)
    merchant_id: int | None = Field(default=None, foreign_key="merchant.id")
    merchant: Merchant | None = Relationship(back_populates="item")

class ItemList(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    items: list[Item]
    page: int
    page_size: int
    size_per_page: int
