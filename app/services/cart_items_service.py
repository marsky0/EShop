from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.database.db import session_manager_for_class

from app.models.cart_items import CartItemOrm
from app.schemas.cart_items import CartItemCreate, CartItemUpdate, CartItemBase, CartItemOpt

class CartItemService:

    @session_manager_for_class
    async def list(self, session: AsyncSession) -> List[CartItemOrm]:
        result = await session.execute(select(CartItemOrm))
        return result.scalars().all()

    @session_manager_for_class
    async def get_by_id(self, session: AsyncSession, id: int) -> CartItemOrm:
        result = await session.execute(select(CartItemOrm).where(CartItemOrm.id == id))
        item = result.scalars().first()
        if not item:
            raise HTTPException(status_code=404, detail="CartItem not found")
        return item

    @session_manager_for_class
    async def get_by_user_id(self, session: AsyncSession, user_id: int) -> List[CartItemOrm]:
        result = await session.execute(select(CartItemOrm).where(CartItemOrm.user_id == user_id))
        items = result.scalars().all()
        return items

    @session_manager_for_class
    async def create(self, session: AsyncSession, data: CartItemCreate) -> CartItemOrm:
        new_cart = CartItemOrm(**data.dict())
        session.add(new_cart)
        try:
            await session.commit()
            await session.refresh(new_cart)
            return new_cart
        except IntegrityError as e:
            await session.rollback()
            raise HTTPException(status_code=500, detail=f"Database integrity error: {str(e.orig)}")

    @session_manager_for_class
    async def create_batch(self, session: AsyncSession, data: List[CartItemCreate]) -> List[CartItemOrm]:
        new_items = [CartItemOrm(**i.dict()) for i in data]
        session.add_all(new_items)
        try:
            await session.commit()
            for item in new_items:
                await session.refresh(item)
            return new_items
        except IntegrityError as e:
            await session.rollback()
            raise HTTPException(status_code=500, detail=f"Database integrity error: {str(e.orig)}")

    @session_manager_for_class
    async def update(self, session: AsyncSession, id: int, data: CartItemUpdate) -> CartItemOrm:
        item = await self.get_by_id.__wrapped__(self, session, id)
        for k, v in data.dict(exclude_unset=True).items():
            setattr(item, k, v)
        try:
            await session.commit()
            return item
        except IntegrityError as e :
            await session.rollback()
            raise HTTPException(status_code=500, detail=f"Database integrity error: {str(e.orig)}")

    @session_manager_for_class
    async def update_batch(self, session: AsyncSession, ids: List[int], data: List[CartItemUpdate]) -> List[CartItemOrm]:
        result = await session.execute(select(CartItemOrm).where(CartItemOrm.id.in_(ids)))
        items = result.scalars().all()
        
        items_map = {item.id: item for item in items}
        for id, update in zip(ids, data):
            item = items_map.get(id)
            if not item:
                raise HTTPException(status_code=404, detail=f"Item {id} not found")
            for k, v in update.dict(exclude_unset=True).items():
                setattr(item, k, v)
        try:
            await session.commit()
            return items
        except IntegrityError as e:
            await session.rollback()
            raise HTTPException(status_code=500, detail=f"Database integrity error: {str(e.orig)}")

    @session_manager_for_class
    async def remove(self, session: AsyncSession, id: int) -> CartItemOrm:
        item = await self.get_by_id.__wrapped__(self, session, id)
        await session.delete(item)
        try:
            await session.commit()
            return item
        except IntegrityError as e:
            await session.rollback()
            raise HTTPException(status_code=500, detail=f"Database integrity error: {str(e.orig)}")

    @session_manager_for_class
    async def remove_batch(self, session: AsyncSession, ids: List[int]) -> List[CartItemOrm]:
        result = await session.execute(select(CartItemOrm).where(CartItemOrm.id.in_(ids)))
        items = result.scalars().all()

        for item in items:
            await session.delete(item)
        try:
            await session.commit()
            return items
        except IntegrityError as e:
            await session.rollback()
            raise HTTPException(status_code=500, detail=f"Database integrity error: {str(e.orig)}")
