from typing import AsyncIterator

from sqlmodel import SQLModel

from sqlalchemy.orm import sessionmaker

from sqlmodel.ext.asyncio.session import AsyncSession

from sqlalchemy.ext.asyncio import create_async_engine

connect_args = {}

engine = None

from .item_model import *
from .user_model import *
from .exchange_model import *
from .transaction_model import *
from .wallet_model import *
from .merchant_model import *

def init_db(settings):
    global engine

    engine = create_async_engine(
        settings.SQLDB_URL,
        future=True,
        connect_args=connect_args,
    )


async def recreate_table():
    async with engine.begin() as conn:
        #await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncIterator[AsyncSession]: 
    async_session = sessionmaker(
        engine, 
        class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session