from fastapi import APIRouter, HTTPException, Depends

from sqlmodel import select, func

from typing import Annotated

from .. import models

from sqlmodel.ext.asyncio.session import AsyncSession

from ..models.item_model import CreatedItem, DBItem, Item, ItemList, UpdatedItem

import math

router = APIRouter(prefix="/items", tags=["Item"])

SIZE_PER_PAGE = 50

@router.post("/{merchant_id}")
async def create_item(
    item: CreatedItem,
    session: Annotated[AsyncSession, Depends(models.get_session)],
) -> Item | None:
    data = item.dict()
    dbitem = DBItem(**data)
    session.add(dbitem)
    await session.commit()
    await session.refresh(dbitem)

    return Item.from_orm(dbitem)

@router.get("")
async def get_items(
    session: Annotated[AsyncSession, Depends(models.get_session)],
    page: int = 1,
    size_per_page: int = SIZE_PER_PAGE,
) -> ItemList:
    result = await session.exec(select(DBItem).offset((page - 1) * size_per_page).limit(size_per_page))
    item = result.all()
    page_count = int(
        math.ceil(
           (await session.exec(select(func.count(DBItem.id)))).first()
            / SIZE_PER_PAGE
        )
    )
    return ItemList.from_orm(
        dict(items=item, page_count=page_count, page=page, size_per_page=size_per_page)
    )


@router.get("/{item_id}")
async def get_item(
    item_id: int, session: Annotated[AsyncSession, Depends(models.get_session)]
) -> Item:
    db_item = await session.get(DBItem, item_id)
    if db_item:
        return Item.from_orm(db_item)

    raise HTTPException(status_code=404, detail="Item not found")


@router.put("/{item_id}")
async def update_item(
    item_id: int,
    item: UpdatedItem,
    session: Annotated[AsyncSession, Depends(models.get_session)],
) -> Item:
    print("update_item", item)
    data = item.dict()
    db_item = await session.get(DBItem, item_id)
    db_item.sqlmodel_update(data)
    session.add(db_item)
    await session.commit()
    await session.refresh(db_item)

    return Item.from_orm(db_item)

@router.delete("/{item_id}")
async def delete_item(
    item_id: int, 
    session: Annotated[AsyncSession, Depends(models.get_session)],
) -> dict:
    db_item = await session.get(DBItem, item_id)
    await session.delete(db_item)
    await session.commit()

    return dict(message="Item delete success")