import pytest
from app.schemas.users import UserCreate
from app.schemas.orders import OrderCreate, OrderUpdate, OrderStatus
from app.services.user_service import UserService
from app.services.order_service import OrderService
from app.tests.utils import get_client


@pytest.mark.asyncio
async def test_orders_list():
    client = await get_client()
    order_service = OrderService()

    order = await order_service.create(OrderCreate(user_id=None, product_id=None, quantity=1, status=OrderStatus.new))

    resp = await client.get("/api/orders/")
    assert resp.status_code == 200
    assert any(o["id"] == order.id for o in resp.json())


@pytest.mark.asyncio
async def test_orders_get_by_id():
    client = await get_client()
    user_service = UserService()
    order_service = OrderService()

    user_data = {
        "username": "orders_user_get",
        "email": "orders_user_get@example.com",
        "password": "pass123",
        "is_confirmed": True
    }
    admin_data = {
        "username": "orders_admin_get",
        "email": "orders_admin_get@example.com",
        "password": "pass123",
        "is_confirmed": True,
        "is_admin": True
    }

    await user_service.create(UserCreate(**user_data))
    await user_service.create(UserCreate(**admin_data))

    user_token = (await client.post("/api/auth/login", json={
        "email": user_data["email"], 
        "password": user_data["password"]
    })).json()
    admin_token = (await client.post("/api/auth/login", json={
        "email": admin_data["email"], 
        "password": admin_data["password"]
    })).json()

    order_user = await order_service.create(OrderCreate(user_id=user_token["user_id"], product_id=None, quantity=1, status=OrderStatus.new))
    order_admin = await order_service.create(OrderCreate(user_id=admin_token["user_id"], product_id=None, quantity=1, status=OrderStatus.new))

    resp = await client.get(f"/api/orders/{order_user.id}", headers={
        "Authorization": f"Bearer {user_token['access_token']}"
    })
    assert resp.status_code == 200
    assert resp.json()["id"] == order_user.id

    resp = await client.get(f"/api/orders/{order_admin.id}", headers={
        "Authorization": f"Bearer {user_token['access_token']}"
    })
    assert resp.status_code == 403

    resp = await client.get(f"/api/orders/{order_user.id}", headers={
        "Authorization": f"Bearer {admin_token['access_token']}"
    })
    assert resp.status_code == 200

    resp = await client.get(f"/api/orders/{order_admin.id}", headers={
        "Authorization": f"Bearer {admin_token['access_token']}"
    })
    assert resp.status_code == 200


@pytest.mark.asyncio
async def test_orders_create():
    client = await get_client()
    user_service = UserService()

    user_data = {
        "username": "orders_user_create",
        "email": "orders_user_create@example.com",
        "password": "pass123",
        "is_confirmed": True
    }
    admin_data = {
        "username": "orders_admin_create",
        "email": "orders_admin_create@example.com",
        "password": "pass123",
        "is_confirmed": True,
        "is_admin": True
    }

    await user_service.create(UserCreate(**user_data))
    await user_service.create(UserCreate(**admin_data))

    user_token = (await client.post("/api/auth/login", json={
        "email": user_data["email"], 
        "password": user_data["password"]
    })).json()
    admin_token = (await client.post("/api/auth/login", json={
        "email": admin_data["email"], 
        "password": admin_data["password"]
    })).json()

    payload = {
        "user_id": user_token["user_id"],
        "product_id": None,
        "quantity": 2,
        "status": OrderStatus.new
    }

    bad_payload = payload.copy()
    bad_payload["user_id"] = admin_token["user_id"]
    resp = await client.post("/api/orders/", json=bad_payload, headers={
        "Authorization": f"Bearer {user_token['access_token']}"
    })
    assert resp.status_code == 403

    resp = await client.post("/api/orders/", json=payload, headers={
        "Authorization": f"Bearer {user_token['access_token']}"
    })
    assert resp.status_code == 200
    assert resp.json()["quantity"] == payload["quantity"]

    admin_payload = payload.copy()
    admin_payload["user_id"] = user_token["user_id"]
    resp = await client.post("/api/orders/", json=admin_payload, headers={
        "Authorization": f"Bearer {admin_token['access_token']}"
    })
    assert resp.status_code == 200


@pytest.mark.asyncio
async def test_orders_update():
    client = await get_client()
    user_service = UserService()
    order_service = OrderService()

    user_data = {
        "username": "orders_user_update",
        "email": "orders_user_update@example.com",
        "password": "pass123",
        "is_confirmed": True
    }
    admin_data = {
        "username": "orders_admin_update",
        "email": "orders_admin_update@example.com",
        "password": "pass123",
        "is_confirmed": True,
        "is_admin": True
    }

    await user_service.create(UserCreate(**user_data))
    await user_service.create(UserCreate(**admin_data))

    user_token = (await client.post("/api/auth/login", json={
        "email": user_data["email"], 
        "password": user_data["password"]
    })).json()
    admin_token = (await client.post("/api/auth/login", json={
        "email": admin_data["email"], 
        "password": admin_data["password"]
    })).json()

    order_user = await order_service.create(OrderCreate(user_id=user_token["user_id"], product_id=None, quantity=1, status=OrderStatus.new))
    order_admin = await order_service.create(OrderCreate(user_id=admin_token["user_id"], product_id=None, quantity=1, status=OrderStatus.new))

    update_data = {"quantity": 5, "status": OrderStatus.processing}

    resp = await client.put(f"/api/orders/{order_admin.id}", json=update_data, headers={
        "Authorization": f"Bearer {user_token['access_token']}"
    })
    assert resp.status_code == 403

    resp = await client.put(f"/api/orders/{order_user.id}", json=update_data, headers={
        "Authorization": f"Bearer {user_token['access_token']}"
    })
    assert resp.status_code == 200
    assert resp.json()["quantity"] == update_data["quantity"]
    assert resp.json()["status"] == update_data["status"]

    resp = await client.put(f"/api/orders/{order_user.id}", json=update_data, headers={
        "Authorization": f"Bearer {admin_token['access_token']}"
    })
    assert resp.status_code == 200


@pytest.mark.asyncio
async def test_orders_remove():
    client = await get_client()
    user_service = UserService()
    order_service = OrderService()

    user_data = {
        "username": "orders_user_remove",
        "email": "orders_user_remove@example.com",
        "password": "pass123",
        "is_confirmed": True
    }
    admin_data = {
        "username": "orders_admin_remove",
        "email": "orders_admin_remove@example.com",
        "password": "pass123",
        "is_confirmed": True,
        "is_admin": True
    }

    await user_service.create(UserCreate(**user_data))
    await user_service.create(UserCreate(**admin_data))

    user_token = (await client.post("/api/auth/login", json={
        "email": user_data["email"], 
        "password": user_data["password"]
    })).json()
    admin_token = (await client.post("/api/auth/login", json={
        "email": admin_data["email"], 
        "password": admin_data["password"]
    })).json()

    order = await order_service.create(OrderCreate(user_id=user_token["user_id"], product_id=None, quantity=1, status=OrderStatus.new))

    resp = await client.delete(f"/api/orders/{order.id}", headers={
        "Authorization": f"Bearer {admin_token['access_token']}" 
    })
    assert resp.status_code == 200

    order2 = await order_service.create(OrderCreate(user_id=user_token["user_id"], product_id=None, quantity=1, status=OrderStatus.new))
    resp = await client.delete(f"/api/orders/{order2.id}", headers={
        "Authorization": f"Bearer {user_token['access_token']}"
    })
    assert resp.status_code == 200
