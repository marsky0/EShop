from fastapi import APIRouter, HTTPException

from app.auth.oauth import register_for_confirm_token, register_confirm_for_jwt_token_pair, login_for_jwt_token_pair, logout_by_token, refresh_jwt_token_pair_by_token
from app.schemas.auth import JwtTokenPairOpt, LoginOpt, RegisterOpt, TokenOpt
from app.tasks import email
from app.core.config import settings


router = APIRouter(prefix="/api/auth")

@router.post("/register")
async def register(data: RegisterOpt):
    token = await register_for_confirm_token(data)
    email.send_confirmation_email.delay(data.email, token)
    return {"msg": "The letter has been sent"}

@router.get("/confirm/{token}", response_model=JwtTokenPairOpt)
async def confirm(token: str):
    return await register_confirm_for_jwt_token_pair(token)

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
