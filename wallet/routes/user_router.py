from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from typing import Annotated

from .. import deps
from .. import models
from ..models.user_model import ChangedPassword, RegisteredUser, UpdatedUser, User, DBUser

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/create")
async def create_user(
    user_info: RegisteredUser,
    session: Annotated[AsyncSession, Depends(models.get_session)],
) -> User:

    result = await session.exec(
        select(DBUser).where(DBUser.username == user_info.username)
    )

    user = result.one_or_none()

    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This username is exists.",
        )

    user = DBUser.from_orm(user_info)
    await user.set_password(user_info.password)
    session.add(user)
    await session.commit()

    return user

@router.get("/me")
def get_me(current_user: User = Depends(deps.get_current_user)) -> User:
    return current_user


@router.get("/{user_id}")
async def get(
    user_id: int,
    session: Annotated[AsyncSession, Depends(models.get_session)],
) -> User:

    user = await session.get(DBUser, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found this user",
        )
    return user

@router.put("/{user_id}/change_password")
async def change_password(
    session: Annotated[AsyncSession, Depends(models.get_session)],
    user_id: int,
    password_update: ChangedPassword,
) -> dict(): # type: ignore

    user = await session.get(DBUser, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found this user",
        )

    if not user.verify_password(password_update.current_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
        )

    await user.set_password(password_update.new_password)
    session.add(user)
    await session.commit()


@router.put("/{user_id}/update")
async def update_user(
    session: Annotated[AsyncSession, Depends(models.get_session)],
    user_id: int,
    user_update: UpdatedUser,
) -> User:

    user = await session.get(DBUser, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found this user",
        )

    if not user.verify_password(user_update.verify_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
        )

    set_dict = user_update.dict()
    user.sqlmodel_update(set_dict)
    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user