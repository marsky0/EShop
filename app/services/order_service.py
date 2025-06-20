from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.database.db import session_manager_for_class

from app.models.orders import OrderOrm
from app.schemas.orders import OrderCreate, OrderUpdate

class OrderService:
    
    @session_manager_for_class
    async def list(self, session: AsyncSession) -> List[OrderOrm]:
        result = await session.execute(select(OrderOrm))
        return result.scalars().all()

    @session_manager_for_class
    async def get_by_id(self, session: AsyncSession, id: int) -> OrderOrm:
        stmt = select(OrderOrm).where(OrderOrm.id == id)
        result = await session.execute(stmt)
        order = result.scalars().first()
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        return order
    
    @session_manager_for_class
    async def create(self, session: AsyncSession, data: OrderCreate) -> OrderOrm:
        new_order = OrderOrm(**data.dict())
        session.add(new_order)
        try:
            await session.commit()
            await session.refresh(new_order)
            return new_order
        except IntegrityError as e:
            await session.rollback()
            raise HTTPException(status_code=500, detail=f"Database integrity error: {str(e.orig)}")

    @session_manager_for_class
    async def update(self, session: AsyncSession, id: int, data: OrderUpdate) -> OrderOrm:
        order = await self.get_by_id.__wrapped__(self, session, id)
        for k, v in data.dict(exclude_unset=True).items():
            setattr(order, k, v)
        try:
            await session.commit()
            return order
        except IntegrityError as e:
            await session.rollback()
            raise HTTPException(status_code=500, detail=f"Database integrity error: {str(e.orig)}")

    @session_manager_for_class
    async def remove(self, session: AsyncSession, id: int) -> OrderOrm:
        order = await self.get_by_id.__wrapped__(self, session, id)
        await session.delete(order)
        try:
            await session.commit()
            return order
        except IntegrityError as e:
            await session.rollback()
            raise HTTPException(status_code=500, detail=f"Database integrity error: {str(e.orig)}")
