from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from jwt.exceptions import InvalidTokenError
from typing import Optional

import jwt
import uuid

from app.database.db import session_manager
from app.models.users import UserOrm
from app.models.auth import JwtTokenPairOrm
from app.schemas.auth import LoginOpt, RegisterOpt, TokenData, TokenOpt
from app.core.config import settings
from app.utils.hash import generate_hash, validate_hash
from app.utils.datetime import current_timestamp

credentials_exception = HTTPException(
    status_code=401, 
    detail="Could not validate credentials", 
    headers={"WWW-Authenticate": "Bearer"}
)

token_expired_exception = HTTPException(
    status_code=401, 
    detail="Token already expired", 
    headers={"WWW-Authenticate": "Bearer"}
)

@session_manager
async def create_jwt_token_pair(session: AsyncSession, user_id: int) -> JwtTokenPairOrm:
    token_uuid = str(uuid.uuid4())

    access_expires_timestamp = current_timestamp() + settings.access_token_expires
    to_encode = {"uuid": token_uuid, "type": "access", "user_id": user_id, "expire": access_expires_timestamp}
    encoded_access_token = jwt.encode(to_encode, settings.secret_key, algorithm=settings.jwt_algorithm)

    refresh_expires_timestamp = current_timestamp() + settings.refresh_token_expires
    to_encode = {"uuid": token_uuid, "type": "refresh", "user_id": user_id, "expire": refresh_expires_timestamp}
    encoded_refresh_token = jwt.encode(to_encode, settings.secret_key, algorithm=settings.jwt_algorithm)

    jwt_token_pair = JwtTokenPairOrm(
        uuid=token_uuid, 
        user_id=user_id, 
        access_token=encoded_access_token,
        refresh_token=encoded_refresh_token,
        access_token_expires_timestamp=access_expires_timestamp,
        refresh_token_expires_timestamp=refresh_expires_timestamp
    )

    try:
        session.add(jwt_token_pair)
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Database integrity error")

    return jwt_token_pair

async def create_register_confirm_token(email: str) -> str:
    expires_timestamp = current_timestamp() + 5*60
    to_encode = {"type": "confirm", "email": email, "expire": expires_timestamp}
    token = jwt.encode(to_encode, settings.secret_key, algorithm=settings.jwt_algorithm)
    return token

async def get_token_data(token: str) -> Optional[TokenData]:
    try:
        data = jwt.decode(token, settings.secret_key, algorithms=[settings.jwt_algorithm])
        if data["type"] != "access" and data["type"] != "refresh":
            return None
        return TokenData(**data)
    except InvalidTokenError:
        return None

@session_manager
async def authenticate_user(session: AsyncSession, email: str, password: str) -> Optional[UserOrm]:
    result = await session.execute(
        select(UserOrm).where(UserOrm.email == email)
    )
    user = result.scalars().first()

    if not user or not validate_hash(password, user.password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    return user

@session_manager
async def get_current_user(session: AsyncSession, token: str) -> UserOrm:
    data = await get_token_data(token)
    if not data and data.type != "access":
        raise credentials_exception

    if data.expire < current_timestamp():
        raise token_expired_exception
    
    result = await session.execute(
        select(UserOrm).where(UserOrm.id == data.user_id)
    )
    user = result.scalars().first()

    if not user:
        raise credentials_exception
    
    return user

@session_manager
async def register_for_confirm_token(session: AsyncSession, data: RegisterOpt):
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
        confirm_token = await create_register_confirm_token(data.email)
        return confirm_token
    except IntegrityError as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Database integrity error: {str(e)}")

@session_manager
async def register_confirm_for_jwt_token_pair(session: AsyncSession, data: TokenOpt):
    token_data = jwt.decode(data, settings.secret_key, algorithms=[settings.jwt_algorithm])
    if not token_data or token_data["type"] != "confirm":
        raise HTTPException(status_code=400, detail="Invalid confirm token.")
    
    if token_data["expire"] < current_timestamp():
        raise token_expired_exception
    
    result = await session.execute(select(UserOrm).where(UserOrm.email==token_data["email"]))
    user = result.scalars().first()

    if not user:
        raise credentials_exception
    
    user.is_confirmed = True

    try:
        await session.commit()
        await session.refresh(user)
        jwt_token_pair = await create_jwt_token_pair(user.id)
        return jwt_token_pair
    except IntegrityError as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Database integrity error: {str(e)}")


async def login_for_jwt_token_pair(data: LoginOpt) -> JwtTokenPairOrm:
    user = await authenticate_user(data.email, data.password)
    jwt_token_pair = await create_jwt_token_pair(user.id)
    return jwt_token_pair

@session_manager
async def logout_by_token(session: AsyncSession, token: str):
    token_data = await get_token_data(token)
    if not token_data:
        raise credentials_exception
    
    if token_data.expire < current_timestamp():
        raise token_expired_exception
    
    result = await session.execute(
        select(JwtTokenPairOrm).where(JwtTokenPairOrm.uuid == token_data.uuid)
    )
    token_pair = result.scalars().first()

    if not token_pair:
        raise credentials_exception
    
    if token_pair.is_revoked:
        raise  HTTPException(
            status_code=400, 
            detail="Token already revoked", 
            headers={"WWW-Authenticate": "Bearer"}
        )

    token_pair.is_revoked = True
    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Database integrity error")

@session_manager
async def refresh_jwt_token_pair_by_token(session: AsyncSession, refresh_token: str) -> JwtTokenPairOrm:
    token_data = await get_token_data(refresh_token)
    if not token_data or token_data.type != "refresh":
        raise credentials_exception
    
    if token_data.expire < current_timestamp():
        raise token_expired_exception
    
    result = await session.execute(
        select(JwtTokenPairOrm).where(JwtTokenPairOrm.uuid == token_data.uuid)
    )
    token = result.scalars().first()
    if not token:
        raise credentials_exception
    
    if token.is_revoked:
        result = await session.execute(
            select(JwtTokenPairOrm).where(JwtTokenPairOrm.user_id == token_data.user_id)
        )
        tokens = result.scalars().all()
        for t in tokens:
            t.is_revoked = True
        try:
            await session.commit()
        except IntegrityError:
            await session.rollback()
            raise HTTPException(status_code=500, detail=f"Database integrity error")
        
        raise HTTPException(status_code=400, detail="Token already revoked")
    
    token.is_revoked = True
    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Database integrity error")
    
    new_token_pair = await create_jwt_token_pair(token_data.user_id)
    return new_token_pair

async def authorization_user_by_headers(headers):
    data = headers.get("Authorization")
    if not data:
        raise HTTPException(
            status_code=401, 
            detail="Not authenticated", 
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    data = data.split()
    if not data:
        raise HTTPException(
            status_code=401, 
            detail="Not authenticated", 
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    user = await get_current_user(data[-1])
    if not user:
        raise HTTPException(
            status_code=404,
            detail="Account not found",
            headers={"WWW-Authenticate": "Bearer"}
        )

    if not user.is_confirmed:
        raise HTTPException(
            status_code=401,
            detail="Account not verified",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    return user