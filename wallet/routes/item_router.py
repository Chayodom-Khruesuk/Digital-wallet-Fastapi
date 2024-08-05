from fastapi import APIRouter, HTTPException

from sqlmodel import Session, select

from models.item_models import Item, ItemList, DBItem, CreatedItem, UpdatedItem

from models.database import engine

router = APIRouter()

@router.post("/item/{merchant_id}", tags=["Item"])
async def create_item(item: CreatedItem, merchant_id: int) -> Item:
    data = item.dict()
    db_item = DBItem(**data)
    db_item.merchant_id = merchant_id
    with Session(engine) as db:
        db.add(db_item)
        db.commit()
        db.refresh(db_item)

    return Item.from_orm(db_item)


@router.get("/item", tags=["Item"])
async def get_items(page: int = 1, page_size: int = 10) -> ItemList:
    with Session(engine) as db:
        db_items = db.exec(
            select(DBItem).offset((page - 1) * page_size).limit(page_size)
        ).all()


@router.get("/item/{item_id}", tags=["Item"])
async def get_item(item_id: int) -> Item:
    with Session(engine) as db:
        db_item = db.get(DBItem, item_id)
        if db_item is None:
            raise HTTPException(status_code=404, detail="Item not found")
        return Item.from_orm(db_item)


@router.put("/item/{item_id}", tags=["Item"])
async def update_item(item_id: int, item: UpdatedItem) -> Item:
    with Session(engine) as db:
        db_item = db.get(DBItem, item_id)
        if db_item is None:
            raise HTTPException(status_code=404, detail="Item not found")
        for key, value in item.dict().items():
            setattr(db_item, key, value)
            db.add(db_item)
            db.commit()
            db.refresh(db_item)

    return Item.from_orm(db_item)


@router.delete("/item/{item_id}", tags=["Item"])
async def delete_item(item_id: int) -> dict:
    with Session(engine) as db:
        db_item = db.get(DBItem, item_id)
        if db_item is None:
            raise HTTPException(status_code=404, detail="Item not found")
        db.delete(db_item)
        db.commit()

    return dict(message="Item deleted successfully")