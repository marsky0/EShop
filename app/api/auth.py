from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi_limiter.depends import RateLimiter

from app.auth.oauth import register_for_confirm_token, register_confirm_for_jwt_token_pair, login_for_jwt_token_pair, logout_by_token, refresh_jwt_token_pair_by_token
from app.schemas.auth import JwtTokenPairOpt, LoginOpt, RegisterOpt, TokenOpt
from app.tasks import email
from app.core.config import settings


router = APIRouter(prefix="/api/auth")

@router.post("/register", dependencies=[Depends(RateLimiter(times=25, seconds=60))])
async def register(data: RegisterOpt):
    token = await register_for_confirm_token(data)
    email.send_confirmation_email.delay(data.email, token)
    return {"msg": "The letter has been sent"}

@router.get("/confirm/{token}", response_model=JwtTokenPairOpt, dependencies=[Depends(RateLimiter(times=25, seconds=60))])
async def confirm(token: str):
    return await register_confirm_for_jwt_token_pair(token)

@router.post("/login", response_model=JwtTokenPairOpt, dependencies=[Depends(RateLimiter(times=25, seconds=60))])
async def login(data: LoginOpt):
    return await login_for_jwt_token_pair(data)

@router.post("/logout", dependencies=[Depends(RateLimiter(times=25, seconds=60))])
async def logout(data: TokenOpt):
    await logout_by_token(data.token)
    return {"msg": "Successful logout"}

@router.post("/refresh", response_model=JwtTokenPairOpt, dependencies=[Depends(RateLimiter(times=25, seconds=60))])
async def refresh(data: TokenOpt):
    return await refresh_jwt_token_pair_by_token(data.token)
