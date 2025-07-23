from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.database.db import session_manager_for_class

from app.models.comments import CommentOrm
from app.schemas.comments import CommentCreate, CommentUpdate

class CommentService:
    
    @session_manager_for_class
    async def list(self, session: AsyncSession) -> List[CommentOrm]:
        result = await session.execute(select(CommentOrm))
        return result.scalars().all()

    @session_manager_for_class
    async def get_by_id(self, session: AsyncSession, id: int) -> CommentOrm:
        result = await session.execute(select(CommentOrm).where(CommentOrm.id == id))
        comment = result.scalars().first()
        if not comment:
            raise HTTPException(status_code=404, detail="Comment not found")
        return comment
    
    @session_manager_for_class
    async def create(self, session: AsyncSession, data: CommentCreate) -> CommentOrm:
        new_comment = CommentOrm(**data.model_dump())
        session.add(new_comment)
        try:
            await session.commit()
            await session.refresh(new_comment)
            return new_comment
        except IntegrityError as e:
            await session.rollback()
            raise HTTPException(status_code=500, detail=f"Database integrity error: {str(e.orig)}")

    @session_manager_for_class
    async def update(self, session: AsyncSession, id: int, data: CommentUpdate) -> CommentOrm:
        comment = await self.get_by_id.__wrapped__(self, session, id)
        for k, v in data.model_dump(exclude_unset=True).items():
            setattr(comment, k, v)
        try:
            await session.commit()
            return comment
        except IntegrityError as e:
            await session.rollback()
            raise HTTPException(status_code=500, detail=f"Database integrity error: {str(e.orig)}")

    @session_manager_for_class
    async def remove(self, session: AsyncSession, id: int) -> CommentOrm:
        comment = await self.get_by_id.__wrapped__(self, session, id)
        await session.delete(comment)
        try:
            await session.commit()
            return comment
        except IntegrityError as e:
            await session.rollback()
            raise HTTPException(status_code=500, detail=f"Database integrity error: {str(e.orig)}")


