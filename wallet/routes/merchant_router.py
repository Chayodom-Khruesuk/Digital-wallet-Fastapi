from fastapi import APIRouter, HTTPException, Depends

from sqlmodel import select

from ..models.merchant_model import CreatedMerchant, DBMerchant, Merchant, MerchantList, UpdatedMerchant

from typing import Annotated

from .. import models

from sqlmodel.ext.asyncio.session import AsyncSession

router = APIRouter(prefix="/merchants", tags=["Merchant"])

@router.post("")
async def create_merchant(
    merchant: CreatedMerchant, 
    session: Annotated[AsyncSession, Depends(models.get_session)],
) -> Merchant:
    db_merchant = DBMerchant(**merchant.dict())
    session.add(db_merchant)
    await session.commit()
    await session.refresh(db_merchant)

    return Merchant.from_orm(db_merchant)

@router.get("")
async def read_merchants(
    session: Annotated[AsyncSession, Depends(models.get_session)],
) -> MerchantList:
    merchants = await session.exec(select(DBMerchant)).all()

    return MerchantList.from_orm(
        dict(merchants=merchants, page=0, page_size=0, size_per_page=0)
    )

@router.get("/{merchant_id}")
async def get_merchant(
    merchant_id: int,
    session: Annotated[AsyncSession, Depends(models.get_session)],
) -> Merchant:
    db_merchant = await session.get(DBMerchant, merchant_id)
    if db_merchant is None:
        return Merchant.from_orm(db_merchant)
    
    raise HTTPException(status_code=404, detail="Merchant not found")

@router.put("/{merchant_id}")
async def update_merchant(
    merchant_id: int, 
    merchant: UpdatedMerchant,
    session: Annotated[AsyncSession, Depends(models.get_session)],
) -> Merchant:
    db_merchant = await session.get(DBMerchant, merchant_id)
    db_merchant.sqlmodel_update(**merchant.dict())
    session.add(db_merchant)
    await session.commit()
    await session.refresh(db_merchant)

    return Merchant.from_orm(db_merchant)

@router.delete("/{merchant_id}")
async def delete_merchant(
    merchant_id: int,
    session: Annotated[AsyncSession, Depends(models.get_session)],
    ) -> dict:
    db_merchant = await session.get(DBMerchant, merchant_id)
    await session.delete(db_merchant)
    await session.commit()

    return dict(message="Merchant delete success")
