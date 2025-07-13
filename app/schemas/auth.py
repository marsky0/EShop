from pydantic import BaseModel, Field

from app.utils.datetime import current_timestamp

class JwtTokenPairBase(BaseModel):
    id: int
    uuid: str
    create_timestamp: int = Field(default_factory=current_timestamp)
    update_timestamp: int = Field(default_factory=current_timestamp)
    user_id: int
    access_token: str
    refresh_token: str
    access_token_expires_timestamp: int
    refresh_token_expires_timestamp: int
    is_revoked: bool = False

    class Config:
        from_attributes = True


class JwtTokenPairOpt(BaseModel):
    access_token: str
    refresh_token: str
    access_token_expires_timestamp: int
    refresh_token_expires_timestamp: int
    
    class Config:
        from_attributes = True

class TokenData(BaseModel):
    uuid: str
    type: str
    user_id: int
    expire: int

    class Config:
        from_attributes = True

class TokenOpt(BaseModel):
    token: str

    class Config:
        from_attributes = True

class RegisterOpt(BaseModel):
    username: str
    email: str
    password: str

    class Config:
        from_attributes = True

class LoginOpt(BaseModel):
    email: str
    password: str

    class Config:
        from_attributes = True

