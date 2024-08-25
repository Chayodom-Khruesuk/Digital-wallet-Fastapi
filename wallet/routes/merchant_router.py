from fastapi import APIRouter, HTTPException, Depends

from sqlmodel import select

from wallet import deps

from ..models.merchant_model import CreatedMerchant, DBMerchant, Merchant, MerchantList, UpdatedMerchant

from typing import Annotated

from ..models import user_model
from .. import models

from sqlmodel.ext.asyncio.session import AsyncSession

router = APIRouter(prefix="/merchants", tags=["Merchant"])

@router.post("")
async def create_merchant(
    merchant: CreatedMerchant, 
    session: Annotated[AsyncSession, Depends(models.get_session)],
    current_user: Annotated[user_model.User, Depends(deps.get_current_user)],
) -> Merchant:
    db_merchant = DBMerchant.model_validate(merchant)
    
    db_merchant.user = current_user
    session.add(db_merchant)
    await session.commit()
    await session.refresh(db_merchant)

    return Merchant.model_validate(db_merchant)

@router.get("/{merchant_id}")
async def get_wallet(
    merchant_id: int,
    session: Annotated[AsyncSession, Depends(models.get_session)],
) -> Merchant:
    db_wallet = await session.get(DBMerchant, merchant_id)
    if db_wallet is None:
        raise HTTPException(status_code=404, detail="Merchant not found")
    
    return Merchant.model_validate(db_wallet)

@router.get("")
async def get_merchants(
    session: Annotated[AsyncSession, Depends(models.get_session)],
    page: int = 1,
    page_size: int = 10,
) -> MerchantList:
    result = await session.exec(
        select(DBMerchant).offset((page - 1) * page_size).limit(page_size)
    )
    db_merchants = result.all()

    return MerchantList(
        merchants=db_merchants,
        page=page,
        page_size=page_size,
        size_per_page=len(db_merchants),
    )

@router.put("/{merchant_id}")
async def update_merchant(
    merchant_id: int, 
    merchant: UpdatedMerchant,
    session: Annotated[AsyncSession, Depends(models.get_session)],
) -> Merchant:
    data = merchant.dict()
    db_merchant = await session.get(DBMerchant, merchant_id)
    db_merchant.sqlmodel_update(data)
    session.add(db_merchant)
    await session.commit()
    await session.refresh(db_merchant)

    return Merchant.model_validate(db_merchant)

@router.delete("/{merchant_id}")
async def delete_merchant(
    merchant_id: int,
    session: Annotated[AsyncSession, Depends(models.get_session)],
    ) -> dict:
    db_merchant = await session.get(DBMerchant, merchant_id)
    await session.delete(db_merchant)
    await session.commit()

    return dict(message="Merchant delete success")
