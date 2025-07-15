from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.database.db import session_manager_for_class

from app.models.users import UserOrm
from app.schemas.users import UserCreate, UserUpdate
from app.utils.hash import generate_hash

class UserService:

    @session_manager_for_class
    async def list(self, session: AsyncSession) -> List[UserOrm]:
        result = await session.execute(select(UserOrm))
        return result.scalars().all()

    @session_manager_for_class
    async def get_by_id(self, session: AsyncSession, id: int) -> UserOrm:
        result = await session.execute(select(UserOrm).where(UserOrm.id == id))
        user = result.scalars().first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    
    @session_manager_for_class
    async def get_by_email(self, session: AsyncSession, email: str) -> UserOrm:
        result = await session.execute(select(UserOrm).where(UserOrm.email == email))
        user = result.scalars().first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    
    @session_manager_for_class
    async def get_by_username(self, session: AsyncSession, username: str) -> UserOrm:
        result = await session.execute(select(UserOrm).where(UserOrm.username == username))
        user = result.scalars().first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    @session_manager_for_class
    async def create(self, session: AsyncSession, data: UserCreate) -> UserOrm:
        result = await session.execute(select(UserOrm).where(UserOrm.email==data.email))
        check_email = result.scalars().first()
        if check_email:
            raise HTTPException(status_code=409, detail="Email already registered")

        data.password = generate_hash(data.password)
        new_user = UserOrm(**data.dict())
        session.add(new_user)
        try:
            await session.commit()
            await session.refresh(new_user)
            return new_user
        except IntegrityError as e:
            await session.rollback()
            raise HTTPException(status_code=500, detail=f"Database integrity error: {str(e.orig)}")

    @session_manager_for_class
    async def update(self, session: AsyncSession, id: int, data: UserUpdate) -> UserOrm:
        user = await self.get_by_id.__wrapped__(self, session, id)
        if data.password:
            data.password = generate_hash(data.password) 
        for k, v in data.dict(exclude_unset=True).items():
            setattr(user, k, v)
        try:
            await session.commit()
            return user
        except IntegrityError as e:
            await session.rollback()
            raise HTTPException(status_code=500, detail=f"Database integrity error: {str(e.orig)}")

    @session_manager_for_class
    async def remove(self, session: AsyncSession, id: int) -> UserOrm:
        user = await self.get_by_id.__wrapped__(self, session, id)
        await session.delete(user)
        try:
            await session.commit()
            return user
        except IntegrityError as e:
            await session.rollback()
            raise HTTPException(status_code=500, detail=f"Database integrity error: {str(e.orig)}")

