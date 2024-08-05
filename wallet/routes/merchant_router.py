from fastapi import APIRouter, HTTPException

from sqlmodel import Session, select

from models.item_models import BaseItem
from models.merchant_model import CreatedMerchant, DBMerchant, Merchant, MerchantList, UpdatedMerchant

from models import engine
from routes.item_router import create_item

router = APIRouter(prefix="/merchants", tags=["merchant"])

@router.post("")
async def create_merchant(item: CreatedMerchant) -> Merchant:
    data = item.dict()
    db_merchant = DBMerchant(**data)
    with Session(engine) as session:
        session.add(db_merchant)
        session.commit()
        session.refresh(db_merchant)

    return Merchant.from_orm(db_merchant)


@router.get("")
async def get_merchants(page: int = 1, page_size: int = 10) -> MerchantList:
    with Session(engine) as session:
        db_merchants = session.exec(
            select(DBMerchant).offset((page - 1) * page_size).limit(page_size)
        ).all()

    return MerchantList(
        merchants=db_merchants,
        page=page,
        page_size=page_size,
        size_per_page=len(db_merchants),
    )


@router.get("/{merchant_id}")
async def get_merchant(merchant_id: int) -> Merchant:
    with Session(engine) as session:
        db_merchant = session.get(DBMerchant, merchant_id)
        if db_merchant is None:
            raise HTTPException(status_code=404, detail="Item not found")

    return Merchant.from_orm(db_merchant)


@router.put("/{merchant_id}")
async def update_merchant(merchant_id: int, merchant: UpdatedMerchant) -> Merchant:
    with Session(engine) as session:
        db_merchant = session.get(DBMerchant, merchant_id)
        if db_merchant is None:
            raise HTTPException(status_code=404, detail="Item not found")
        for key, value in merchant.dict().items():
            setattr(db_merchant, key, value)
        session.add(db_merchant)
        session.commit()
        session.refresh(db_merchant)

    return Merchant.from_orm(db_merchant)


@router.delete("/{merchant_id}")
async def delete_merchant(merchant_id: int) -> dict:
    with Session(engine) as session:
        db_merchant = session.get(DBMerchant, merchant_id)
        if db_merchant is None:
            raise HTTPException(status_code=404, detail="Item not found")
        session.delete(db_merchant)
        session.commit()

    return dict(message="Merchant deleted successfully")
