import pytest
from app.schemas.users import UserCreate
from app.schemas.categories import CategoryCreate
from app.services.user_service import UserService
from app.services.category_service import CategoryService
from app.tests.utils import get_client


@pytest.mark.asyncio
async def test_categories_list():
    client = await get_client()
    category_service = CategoryService()

    category = await category_service.create(CategoryCreate(name="categories_list_name"))

    resp = await client.get("/api/categories/")
    assert resp.status_code == 200
    assert any(cat["id"] == category.id for cat in resp.json())

@pytest.mark.asyncio
async def test_categories_get_by_id():
    client = await get_client()
    service = CategoryService()

    category = await service.create(CategoryCreate(name="categories_get_by_id_name"))

    resp = await client.get(f"/api/categories/{category.id}")
    assert resp.status_code == 200
    assert resp.json()["id"] == category.id

@pytest.mark.asyncio
async def test_categories_create():
    client = await get_client()
    category_service = UserService()

    user_data = {
        "username": "categories_user_create",
        "email": "categories_user_create@example.com",
        "password": "pass123",
        "is_confirmed": True
    }
    admin_data = {
        "username": "categories_admin_create",
        "email": "category_admin_create@example.com",
        "password": "pass123",
        "is_confirmed": True,
        "is_admin": True
    }

    await category_service.create(UserCreate(**user_data))
    await category_service.create(UserCreate(**admin_data))

    user_token = (await client.post("/api/auth/login", json={
        "email": user_data["email"], 
        "password": user_data["password"]
    })).json()
    admin_token = (await client.post("/api/auth/login", json={
        "email": admin_data["email"], 
        "password": admin_data["password"]
    })).json()

    payload = {"name": "categories_create_name"}

    resp = await client.post("/api/categories/", json=payload, headers={
        "Authorization": f"Bearer {user_token['access_token']}"
    })
    assert resp.status_code == 403

    resp = await client.post("/api/categories/", json=payload, headers={
        "Authorization": f"Bearer {admin_token['access_token']}"
    })
    assert resp.status_code == 200
    assert resp.json()["name"] == payload["name"]

@pytest.mark.asyncio
async def test_categories_update():
    client = await get_client()
    user_service = UserService()
    category_service = CategoryService()

    user_data = {
        "username": "categories_user_update",
        "email": "categories_user_update@example.com",
        "password": "pass123",
        "is_confirmed": True
    }
    admin_data = {
        "username": "categories_admin_update",
        "email": "category_admin_update@example.com",
        "password": "pass123",
        "is_confirmed": True,
        "is_admin": True
    }

    await user_service.create(UserCreate(**user_data))
    await user_service.create(UserCreate(**admin_data))

    category = await category_service.create(CategoryCreate(name="categories_update_name"))

    user_token = (await client.post("/api/auth/login", json={
        "email": user_data["email"], "password": user_data["password"]
    })).json()
    admin_token = (await client.post("/api/auth/login", json={
        "email": admin_data["email"], "password": admin_data["password"]
    })).json()

    resp = await client.put(f"/api/categories/{category.id}", json={"name": "categories_user_update_name"}, headers={
        "Authorization": f"Bearer {user_token['access_token']}"
    })
    assert resp.status_code == 403

    resp = await client.put(f"/api/categories/{category.id}", json={"name": "categories_admin_update_name"}, headers={
        "Authorization": f"Bearer {admin_token['access_token']}"
    })
    assert resp.status_code == 200
    assert resp.json()["name"] == "categories_admin_update_name"

@pytest.mark.asyncio
async def test_category_remove():
    client = await get_client()
    user_service = UserService()
    category_service = CategoryService()

    user_data = {
        "username": "categories_user_remove",
        "email": "categories_user_remove@example.com",
        "password": "pass123",
        "is_confirmed": True
    }
    admin_data = {
        "username": "categories_admin_remove",
        "email": "categories_admin_remove@example.com",
        "password": "pass123",
        "is_confirmed": True,
        "is_admin": True
    }

    await user_service.create(UserCreate(**user_data))
    await user_service.create(UserCreate(**admin_data))

    category = await category_service.create(CategoryCreate(name="categories_remove_name"))

    user_token = (await client.post("/api/auth/login", json={
        "email": user_data["email"], "password": user_data["password"]
    })).json()
    admin_token = (await client.post("/api/auth/login", json={
        "email": admin_data["email"], "password": admin_data["password"]
    })).json()

    resp = await client.delete(f"/api/categories/{category.id}", headers={
        "Authorization": f"Bearer {user_token['access_token']}"
    })
    assert resp.status_code == 403

    resp = await client.delete(f"/api/categories/{category.id}", headers={
        "Authorization": f"Bearer {admin_token['access_token']}"
    })
    assert resp.status_code == 200
    assert resp.json()["id"] == category.id