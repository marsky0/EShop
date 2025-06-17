from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.database import session_manager_for_class

from app.models.categories import CategoryOrm
from app.schemas.categories import CategoryCreate, CategoryUpdate

class CategoryService:
    
    @session_manager_for_class
    async def list(self, session: AsyncSession) -> List[CategoryOrm]:
        result = await session.execute(select(CategoryOrm))
        return result.scalars().all()

    @session_manager_for_class
    async def get_by_id(self, session: AsyncSession, id: int) -> CategoryOrm:
        stmt = select(CategoryOrm).where(CategoryOrm.id == id)
        result = await session.execute(stmt)
        category = result.scalars().first()
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        return category

    @session_manager_for_class
    async def create(self, session: AsyncSession, data: CategoryCreate) -> CategoryOrm:
        new_category = CategoryOrm(**data.dict())
        session.add(new_category)
        try:
            await session.commit()
            await session.refresh(new_category)
            return new_category
        except IntegrityError as e:
            session.rollback()
            raise HTTPException(status_code=500, detail=f"Database integrity error: {str(e.orig)}")

    @session_manager_for_class
    async def update(self, session: AsyncSession, id: int, data: CategoryUpdate) -> CategoryOrm:
        category = await self.get_by_id.__wrapped__(self, session, id)
        for k, v in data.dict(exclude_unset=True).items():
            setattr(category, k, v)
        try:
            await session.commit()
            return category
        except IntegrityError as e:
            session.rollback()
            raise HTTPException(status_code=500, detail=f"Database integrity error: {str(e.orig)}")

    @session_manager_for_class
    async def remove(self, session: AsyncSession, id: int) -> CategoryOrm:
        category = await self.get_by_id.__wrapped__(self, session, id)
        await session.delete(category)
        try:
            await session.commit()
            return category
        except IntegrityError as e:
            session.rollback()
            raise HTTPException(status_code=500, detail=f"Database integrity error: {str(e.orig)}")
