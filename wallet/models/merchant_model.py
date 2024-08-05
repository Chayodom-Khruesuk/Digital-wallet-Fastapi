from typing import Optional, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict

from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    from models.item_models import Item

class BaseMerchant(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    description: str | None = None
    telephone: str | None = None
    email: str | None = None
    age: int | None = None

class CreatedMerchant(BaseMerchant):
    pass

class UpdatedMerchant(BaseMerchant):
    pass

class Merchant(BaseMerchant):
    id: int

class DBMerchant(Merchant, SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    items: list["Item"] = Relationship(back_populates="merchant")

class MerchantList(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    merchants: list[Merchant]
    page: int
    page_size: int
    size_per_page: int