from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from sqlmodel.ext.asyncio.session import AsyncSession

from wallet.models.wallet_model import DBWallet

from .. import models

router = APIRouter(prefix="/transfers", tags=["Transfer"])

@router.post("/{transfer}")
async def transfer_money(
    from_wallet_id: int, 
    to_wallet_id: int, 
    amount: float,
    session: Annotated[AsyncSession, Depends(models.get_session)]):
    
    from_wallet = await session.get(DBWallet, from_wallet_id)
    to_wallet = await session.get(DBWallet, to_wallet_id)
    
    if not from_wallet or not to_wallet:
        raise HTTPException(status_code=404, detail="Transfer failed")
    
    if from_wallet.balance < amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")
  
    from_wallet.balance -= amount
    to_wallet.balance += amount

    session.add(from_wallet)
    session.add(to_wallet)
    await session.commit()

    return {"message": "Transfer successful", 
            "from_wallet": from_wallet_id, 
            "to_wallet": to_wallet_id, 
            "amount": amount}



