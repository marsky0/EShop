from fastapi import APIRouter, HTTPException

from app.auth.oauth import register_for_jwt_token_pair, login_for_jwt_token_pair, logout_by_token, refresh_jwt_token_pair_by_token
from app.schemas.auth import JwtTokenPairOpt, LoginOpt, RegisterOpt, TokenOpt
from app.core.config import settings

router = APIRouter(prefix="/api/auth")

@router.post("/register", response_model=JwtTokenPairOpt)
async def register(data: RegisterOpt):
    return await register_for_jwt_token_pair(data)

@router.post("/login", response_model=JwtTokenPairOpt)
async def login(data: LoginOpt):
    return await login_for_jwt_token_pair(data)

@router.post("/logout")
async def logout(data: TokenOpt):
    await logout_by_token(data.token)
    return {"msg": "Successful logout"}

@router.post("/refresh", response_model=JwtTokenPairOpt)
async def refresh(data: TokenOpt):
    return await refresh_jwt_token_pair_by_token(data.token)
