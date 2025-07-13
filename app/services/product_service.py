from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.database.db import session_manager_for_class

from app.models.products import ProductOrm
from app.schemas.products import ProductCreate, ProductUpdate

class ProductService:

    @session_manager_for_class
    async def list(self, session: AsyncSession) -> List[ProductOrm]:
        result = await session.execute(select(ProductOrm))
        return result.scalars().all()

    @session_manager_for_class
    async def get_by_id(self, session: AsyncSession, id: int) -> ProductOrm:
        result = await session.execute(select(ProductOrm).where(ProductOrm.id == id))
        product = result.scalars().first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product
    
    @session_manager_for_class
    async def create(self, session: AsyncSession, data: ProductCreate) -> ProductOrm:
        new_product = ProductOrm(**data.dict())
        session.add(new_product)
        try:
            await session.commit()
            await session.refresh(new_product)
            return new_product
        except IntegrityError as e:
            await session.rollback()
            raise HTTPException(status_code=500, detail=f"Database integrity error: {str(e.orig)}")

    @session_manager_for_class
    async def update(self, session: AsyncSession, id: int, data: ProductUpdate) -> ProductOrm:
        product = await self.get_by_id.__wrapped__(self, session, id)
        for k, v in data.dict(exclude_unset=True).items():
            setattr(product, k, v)
        try:
            await session.commit()
            return product
        except IntegrityError as e:
            await session.rollback()
            raise HTTPException(status_code=500, detail=f"Database integrity error: {str(e.orig)}")

    @session_manager_for_class
    async def remove(self, session: AsyncSession, id: int) -> ProductOrm:
        product = await self.get_by_id.__wrapped__(self, session, id)
        await session.delete(product)
        try:
            await session.commit()
            return product
        except IntegrityError as e:
            await session.rollback()
            raise HTTPException(status_code=500, detail=f"Database integrity error: {str(e.orig)}")
