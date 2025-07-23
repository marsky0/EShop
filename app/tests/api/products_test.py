import pytest
from app.schemas.users import UserCreate
from app.schemas.products import ProductCreate
from app.services.user_service import UserService
from app.services.product_service import ProductService
from app.schemas.categories import CategoryCreate
from app.services.category_service import CategoryService
from app.tests.utils import get_client


@pytest.mark.asyncio
async def test_product_list():
    client = await get_client()
    product_service = ProductService()
    category_service = CategoryService()
    
    category = await category_service.create(CategoryCreate(name="products_list_name"))
    product = await product_service.create(ProductCreate(
        name="products_list_name",
        description="products_list_description",
        price=99.99,
        category_id=category.id,
        image=None
    ))

    resp = await client.get("/api/products/")
    assert resp.status_code == 200
    assert any(p["id"] == product.id for p in resp.json())



@pytest.mark.asyncio
async def test_product_get_by_id():
    client = await get_client()
    product_service = ProductService()
    category_service = CategoryService()

    category = await category_service.create(CategoryCreate(name="products_get_by_id_name"))
    product = await product_service.create(ProductCreate(
        name="products_get_by_id_name",
        description="products_get_by_id_description",
        price=99.99,
        category_id=category.id,
        image=None
    ))

    resp = await client.get(f"/api/products/{product.id}")
    assert resp.status_code == 200
    assert resp.json()["id"] == product.id


@pytest.mark.asyncio
async def test_product_create():
    client = await get_client()
    product_service = UserService()
    category_service = CategoryService()

    user_data = {
        "username": "products_user_create",
        "email": "products_user_create@example.com",
        "password": "pass123",
        "is_confirmed": True
    }
    admin_data = {
        "username": "products_admin_create",
        "email": "products_admin_create@example.com",
        "password": "pass123",
        "is_confirmed": True,
        "is_admin": True
    }

    category = await category_service.create(CategoryCreate(name="products_create_name"))

    await product_service.create(UserCreate(**user_data))
    await product_service.create(UserCreate(**admin_data))

    user_token = (await client.post("/api/auth/login", json={
        "email": user_data["email"],
        "password": user_data["password"]
    })).json()
    admin_token = (await client.post("/api/auth/login", json={
        "email": admin_data["email"],
        "password": admin_data["password"]
    })).json()

    product_payload = {
        "category_id": category.id,
        "name": "products_create_name",
        "description": "products_create_description",
        "price": 49.99,
        "image": None
    }

    resp_user = await client.post("/api/products/", json=product_payload, headers={
        "Authorization": f"Bearer {user_token['access_token']}"
    })
    assert resp_user.status_code == 403

    resp_admin = await client.post("/api/products/", json=product_payload, headers={
        "Authorization": f"Bearer {admin_token['access_token']}"
    })
    assert resp_admin.status_code == 200
    assert resp_admin.json()["name"] == product_payload["name"]


@pytest.mark.asyncio
async def test_product_update():
    client = await get_client()
    user_service = UserService()
    product_service = ProductService()
    category_service = CategoryService()

    user_data = {
        "username": "product_user_update",
        "email": "product_user_update@example.com",
        "password": "pass123",
        "is_confirmed": True
    }
    admin_data = {
        "username": "product_admin_update",
        "email": "product_admin_update@example.com",
        "password": "pass123",
        "is_confirmed": True,
        "is_admin": True
    }

    category = await category_service.create(CategoryCreate(name="products_update_name"))

    await user_service.create(UserCreate(**user_data))
    await user_service.create(UserCreate(**admin_data))

    product = await product_service.create(ProductCreate(
        category_id=category.id,
        name="products_update_name",
        description="products_update_description",
        price=10.0,
        image=None
    ))

    user_token = (await client.post("/api/auth/login", json={
        "email": user_data["email"],
        "password": user_data["password"]
    })).json()
    admin_token = (await client.post("/api/auth/login", json={
        "email": admin_data["email"],
        "password": admin_data["password"]
    })).json()

    update_data = {"name": "products_update_name_updated"}

    resp = await client.put(f"/api/products/{product.id}", json=update_data, headers={
        "Authorization": f"Bearer {user_token['access_token']}"
    })
    assert resp.status_code == 403

    resp = await client.put(f"/api/products/{product.id}", json=update_data, headers={
        "Authorization": f"Bearer {admin_token['access_token']}"
    })
    assert resp.status_code == 200
    assert resp.json()["name"] == update_data["name"]


@pytest.mark.asyncio
async def test_product_delete():
    client = await get_client()
    user_service = UserService()
    product_service = ProductService()
    category_service = CategoryService()

    user_data = {
        "username": "product_user_remove",
        "email": "product_user_remove@example.com",
        "password": "pass123",
        "is_confirmed": True
    }
    admin_data = {
        "username": "product_admin_remove",
        "email": "product_admin_remove@example.com",
        "password": "pass123",
        "is_confirmed": True,
        "is_admin": True
    }

    category = await category_service.create(CategoryCreate(name="products_remove_name"))

    await user_service.create(UserCreate(**user_data))
    await user_service.create(UserCreate(**admin_data))

    product = await product_service.create(ProductCreate(
        name="products_remove_name",
        description="products_remove_description",
        price=5.0,
        category_id=category.id,
        image=None
    ))

    user_token = (await client.post("/api/auth/login", json={
        "email": user_data["email"],
        "password": user_data["password"]
    })).json()
    admin_token = (await client.post("/api/auth/login", json={
        "email": admin_data["email"],
        "password": admin_data["password"]
    })).json()

    resp = await client.delete(f"/api/products/{product.id}", headers={
        "Authorization": f"Bearer {user_token['access_token']}"
    })
    assert resp.status_code == 403

    resp = await client.delete(f"/api/products/{product.id}", headers={
        "Authorization": f"Bearer {admin_token['access_token']}"
    })
    assert resp.status_code == 200
    assert resp.json()["name"] == product.name
