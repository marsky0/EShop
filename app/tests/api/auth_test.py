import pytest
from app.auth.oauth import register_for_confirm_token
from app.schemas.auth import RegisterOpt
from app.tests.utils import get_client

@pytest.mark.asyncio
async def test_auth_register():
    client = await get_client()
    
    response = await client.post("/api/auth/register", json={
        "username": "auth_test_register",
        "email": "auth_test_register@example.com",
        "password": "pass123"
    })
    assert response.status_code == 200
    assert response.json()["msg"] == "The letter has been sent"

@pytest.mark.asyncio
async def test_auth_confirm():
    client = await get_client()
    
    data = {
        "username": "auth_test_confirm", 
        "email": "auth_test_confirm@example.com", 
        "password": "pass123"
    }
    token = await register_for_confirm_token(RegisterOpt(**data))
   
    response = await client.get(f"/api/auth/confirm/{token}")
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data

@pytest.mark.asyncio
async def test_auth_login():
    client = await get_client()
    
    data = {
        "username": "auth_test_login", 
        "email": "auth_test_login@example.com", 
        "password": "pass123"
    }
    token = await register_for_confirm_token(RegisterOpt(**data))
    await client.get(f"/api/auth/confirm/{token}")

    response = await client.post("/api/auth/login", json={
        "email": data["email"],
        "password": data["password"]
    })
    assert response.status_code == 200
    login_tokens = response.json()
    assert "access_token" in login_tokens
    assert "refresh_token" in login_tokens

@pytest.mark.asyncio
async def test_auth_refresh():
    client = await get_client()
    
    data = {
        "username": "auth_test_refresh", 
        "email": "auth_test_refresh@example.com", 
        "password": "pass123"
    }
    token = await register_for_confirm_token(RegisterOpt(**data))
    await client.get(f"/api/auth/confirm/{token}")
    
    login_resp = await client.post("/api/auth/login", json={
        "email": data["email"],
        "password": data["password"]
    })
    login_tokens = login_resp.json()
    
    response = await client.post("/api/auth/refresh", json={
        "token": login_tokens["refresh_token"]
    })
    assert response.status_code == 200
    refresh_tokens = response.json()
    assert "access_token" in refresh_tokens
    assert "refresh_token" in refresh_tokens

@pytest.mark.asyncio
async def test_auth_logout():
    client = await get_client()
    
    data = {
        "username": "auth_test_logout", 
        "email": "auth_test_logout@example.com", 
        "password": "pass123"
    }
    token = await register_for_confirm_token(RegisterOpt(**data))
    await client.get(f"/api/auth/confirm/{token}")
    
    login_resp = await client.post("/api/auth/login", json={
        "email": data["email"],
        "password": data["password"]
    })
    login_tokens = login_resp.json()
    
    refresh_resp = await client.post("/api/auth/refresh", json={
        "token": login_tokens["refresh_token"]
    })
    refresh_tokens = refresh_resp.json()
    
    response = await client.post("/api/auth/logout", json={
        "token": refresh_tokens["refresh_token"]
    })
    assert response.status_code == 200
    assert response.json()["msg"] == "Successful logout"