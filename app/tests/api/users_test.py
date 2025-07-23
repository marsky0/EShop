import pytest
from app.services.user_service import UserService
from app.schemas.users import UserCreate
from app.tests.utils import get_client


@pytest.mark.asyncio
async def test_user_list():
    client = await get_client()
    service = UserService()

    user_data = {
        "username": "user_list",
        "email": "users_list@example.com", 
        "password": "pass123", 
        "is_confirmed": True
    }
    admin_user_data = {
        "username": "users_admin_list", 
        "email": "users_admin_list@example.com", 
        "password": "pass123", 
        "is_confirmed": True, 
        "is_admin": True
    }

    await service.create(UserCreate(**user_data))
    await service.create(UserCreate(**admin_user_data))

    resp_user = await client.post("/api/auth/login", json={
        "email": user_data["email"], 
        "password": user_data["password"]
    })
    resp_admin = await client.post("/api/auth/login", json={
        "email": admin_user_data["email"], 
        "password": admin_user_data["password"]
    })
    tokens_user = resp_user.json()
    tokens_admin = resp_admin.json()

    resp_user = await client.get("/api/users/", headers={
        "Authorization": f"Bearer {tokens_user["access_token"]}"
    })
    resp_admin = await client.get("/api/users/", headers={
        "Authorization": f"Bearer {tokens_admin["access_token"]}"
    })

    assert resp_user.status_code == 403
    assert resp_admin.status_code == 200


@pytest.mark.asyncio
async def test_user_get_by_id():
    client = await get_client()
    service = UserService()

    user_data = {
        "username": "users_user_get_by_id", 
        "email": "users_get_by_id@example.com", 
        "password": "pass123", 
        "is_confirmed": True
    }
    admin_user_data = {
        "username": "users_admin_get_by_id", 
        "email": "users_admin_get_by_id@example.com", 
        "password": "pass123", 
        "is_confirmed": True, 
        "is_admin": True
    }

    await service.create(UserCreate(**user_data))
    await service.create(UserCreate(**admin_user_data))

    resp_user = await client.post("/api/auth/login", json={
        "email": user_data["email"], 
        "password": user_data["password"]
    })
    resp_admin = await client.post("/api/auth/login", json={
        "email": admin_user_data["email"], 
        "password": admin_user_data["password"]
    })
    tokens_user = resp_user.json()
    tokens_admin = resp_admin.json()

    resp = await client.get(f"/api/users/{tokens_user["user_id"]}", headers={
        "Authorization": f"Bearer {tokens_user["access_token"]}"
    })
    assert resp.status_code == 200
    resp = await client.get(f"/api/users/{tokens_admin["user_id"]}", headers={
        "Authorization": f"Bearer {tokens_user["access_token"]}"
    })
    assert resp.status_code == 403

    resp = await client.get(f"/api/users/{tokens_admin["user_id"]}", headers={
        "Authorization": f"Bearer {tokens_admin["access_token"]}"
    })
    assert resp.status_code == 200
    resp = await client.get(f"/api/users/{tokens_user["user_id"]}", headers={
        "Authorization": f"Bearer {tokens_admin["access_token"]}"
    })
    assert resp.status_code == 200


@pytest.mark.asyncio
async def test_user_create():
    client = await get_client()
    service = UserService()

    user_data = {
        "username": "users_user_create", 
        "email": "users_user_create@example.com", 
        "password": "pass123", 
        "is_confirmed": True
    }
    admin_data = {
        "username": "users_admin_create", 
        "email": "users_admin_create@example.com", 
        "password": "pass123", 
        "is_confirmed": True, 
        "is_admin": True
    }

    await service.create(UserCreate(**user_data))
    await service.create(UserCreate(**admin_data))

    user_token = (await client.post("/api/auth/login", json={
        "email": user_data["email"], 
        "password": user_data["password"]
    })).json()
    admin_token = (await client.post("/api/auth/login", json={
        "email": admin_data["email"], 
        "password": admin_data["password"]
    })).json()

    new_user_payload = {
        "username": "users_created_by_test",
        "email": "users_created_by_test@example.com",
        "password": "pass123",
        "is_confirmed": True,
        "is_admin": False
    }

    resp_user = await client.post("/api/users/", json=new_user_payload, headers={
        "Authorization": f"Bearer {user_token['access_token']}"
    })
    assert resp_user.status_code == 403

    resp_admin = await client.post("/api/users/", json=new_user_payload, headers={
        "Authorization": f"Bearer {admin_token['access_token']}"
    })
    assert resp_admin.status_code == 200
    assert resp_admin.json()["email"] == new_user_payload["email"]

@pytest.mark.asyncio
async def test_user_update():
    client = await get_client()
    service = UserService()

    user_data = {
        "username": "users_user_update", 
        "email": "users_user_update@example.com", 
        "password": "pass123", 
        "is_confirmed": True
    }
    admin_data = {
        "username": "users_admin_update", 
        "email": "users_admin_update@example.com", 
        "password": "pass123", "is_confirmed": True, 
        "is_admin": True
    }

    user = await service.create(UserCreate(**user_data))
    admin = await service.create(UserCreate(**admin_data))

    user_token = (await client.post("/api/auth/login", json={
        "email": user_data["email"], 
        "password": user_data["password"]
    })).json()
    admin_token = (await client.post("/api/auth/login", json={
        "email": admin_data["email"], 
        "password": admin_data["password"]
    })).json()

    update_data_user = {"username": "users_user_updated_self"}
    update_data_admin = {"username": "users_admin_updated_user"}

    resp = await client.put(f"/api/users/{user.id}", json=update_data_user, headers={
        "Authorization": f"Bearer {user_token['access_token']}"
    })
    assert resp.status_code == 403

    resp = await client.put(f"/api/users/{admin.id}", json=update_data_admin, headers={
        "Authorization": f"Bearer {user_token['access_token']}"
    })
    assert resp.status_code == 403

    resp = await client.put(f"/api/users/{admin.id}", json=update_data_admin, headers={
        "Authorization": f"Bearer {admin_token['access_token']}"
    })
    assert resp.status_code == 200
    assert resp.json()["username"] == update_data_admin["username"]

    resp = await client.put(f"/api/users/{user.id}", json=update_data_user, headers={
        "Authorization": f"Bearer {admin_token['access_token']}"
    })
    assert resp.status_code == 200
    assert resp.json()["username"] == update_data_user["username"]

@pytest.mark.asyncio
async def test_user_remove():
    client = await get_client()
    service = UserService()

    user_data = {
        "username": "users_user_remove", 
        "email": "users_user_remove@example.com", 
        "password": "pass123", 
        "is_confirmed": True
    }
    admin_data = {
        "username": "users_admin_remove", 
        "email": "users_admin_remove@example.com", 
        "password": "pass123", 
        "is_confirmed": True, 
        "is_admin": True
    }

    target_user = await service.create(UserCreate(
        username="users_user_to_be_removed", 
        email="users_user_to_be_removed@example.com", 
        password="pass123", 
        is_confirmed=True)
    )

    await service.create(UserCreate(**user_data))
    await service.create(UserCreate(**admin_data))

    user_token = (await client.post("/api/auth/login", json={
        "email": user_data["email"], 
        "password": user_data["password"]
    })).json()
    admin_token = (await client.post("/api/auth/login", json={
        "email": admin_data["email"], 
        "password": admin_data["password"]
    })).json()

    resp_user = await client.delete(f"/api/users/{target_user.id}", headers={
        "Authorization": f"Bearer {user_token['access_token']}"
    })
    assert resp_user.status_code == 403

    resp_admin = await client.delete(f"/api/users/{target_user.id}", headers={
        "Authorization": f"Bearer {admin_token['access_token']}"
    })
    assert resp_admin.status_code == 200
    assert resp_admin.json()["email"] == target_user.email