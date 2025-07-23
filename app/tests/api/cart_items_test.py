import pytest
from app.schemas.users import UserCreate
from app.schemas.cart_items import CartItemCreate
from app.schemas.products import ProductCreate
from app.services.user_service import UserService
from app.services.product_service import ProductService
from app.services.cart_item_service import CartItemService
from app.tests.utils import get_client

@pytest.mark.asyncio
async def test_cartitem_list():
    client = await get_client()
    user_service = UserService()
    product_service = ProductService()
    cart_service = CartItemService()

    admin = await user_service.create(UserCreate(
        username="cart_items_admin_list", 
        email="cart_items_admin_list@example.com", 
        password="pass123", 
        is_confirmed=True, 
        is_admin=True
    ))
    product = await product_service.create(ProductCreate(
        name="cart_items_test_prod",
        price=100,
        description="",
        category_id=None,
        image=None
    ))
    item = await cart_service.create(CartItemCreate(user_id=admin.id, product_id=product.id, quantity=2))

    token = (await client.post("/api/auth/login", json={
        "email": admin.email, 
        "password": "pass123"
    })).json()

    resp = await client.get("/api/cart_items/", headers={
        "Authorization": f"Bearer {token['access_token']}"
    })
    assert resp.status_code == 200
    assert any(i["id"] == item.id for i in resp.json())

@pytest.mark.asyncio
async def test_cartitem_get_by_id():
    client = await get_client()
    user_service = UserService()
    product_service = ProductService()
    cart_service = CartItemService()

    admin = await user_service.create(UserCreate(
        username="cart_items_admin_get_by_id", 
        email="cart_items_admin_get@example.com", 
        password="pass123", 
        is_confirmed=True, 
        is_admin=True
    ))
    product = await product_service.create(ProductCreate(
        name="cart_items_test_prod_get_by_id", 
        price=100,
        description="",
        category_id=None,
        image=None
    ))
    item = await cart_service.create(CartItemCreate(user_id=admin.id, product_id=product.id, quantity=2))

    token = (await client.post("/api/auth/login", json={
        "email": admin.email, 
        "password": "pass123"
    })).json()

    resp = await client.get(f"/api/cart_items/{item.id}", headers={
        "Authorization": f"Bearer {token['access_token']}"
    })
    assert resp.status_code == 200
    assert resp.json()["id"] == item.id

@pytest.mark.asyncio
async def test_cartitem_get_by_user_id():
    client = await get_client()
    user_service = UserService()
    product_service = ProductService()
    cart_service = CartItemService()

    user = await user_service.create(UserCreate(
        username="cart_items_user_get_by_id", 
        email="cart_items_user_get_by_id@example.com", 
        password="pass123", 
        is_confirmed=True
    ))
    product = await product_service.create(ProductCreate(
        name="cart_items_get_by_id", 
        price=50,
        description="",
        category_id=None,
        image=None
    ))
    await cart_service.create(CartItemCreate(user_id=user.id, product_id=product.id, quantity=1))

    token = (await client.post("/api/auth/login", json={
        "email": user.email, 
        "password": "pass123"
    })).json()

    resp = await client.get(f"/api/cart_items/user-id/{user.id}", headers={
        "Authorization": f"Bearer {token['access_token']}"
    })
    assert resp.status_code == 200
    assert all(item["user_id"] == user.id for item in resp.json())

@pytest.mark.asyncio
async def test_cartitem_create():
    client = await get_client()
    user_service = UserService()
    product_service = ProductService()

    user = await user_service.create(UserCreate(
        username="cart_items_user_create", 
        email="cart_items_user_create@example.com", 
        password="pass123", 
        is_confirmed=True
    ))
    admin = await user_service.create(UserCreate(
        username="cart_items_admin_create", 
        email="cart_items_admin_create@example.com", 
        password="pass123", 
        is_confirmed=True, 
        is_admin=True
    ))
    product = await product_service.create(ProductCreate(
        name="cart_items_create", 
        price=120,
        description="",
        category_id=None,
        image=None
    ))

    user_token = (await client.post("/api/auth/login", json={"email": user.email, "password": "pass123"})).json()
    admin_token = (await client.post("/api/auth/login", json={"email": admin.email, "password": "pass123"})).json()

    resp = await client.post("/api/cart_items/", json={
        "user_id": admin.id, "product_id": product.id, "quantity": 3
    }, headers={"Authorization": f"Bearer {user_token['access_token']}"})
    assert resp.status_code == 403

    resp = await client.post("/api/cart_items/", json={
        "user_id": user.id, "product_id": product.id, "quantity": 3
    }, headers={"Authorization": f"Bearer {user_token['access_token']}"})
    assert resp.status_code == 200
    assert resp.json()["user_id"] == user.id

    resp = await client.post("/api/cart_items/", json={
        "user_id": user.id, "product_id": product.id, "quantity": 3
    }, headers={"Authorization": f"Bearer {admin_token['access_token']}"})
    assert resp.status_code == 200
    assert resp.json()["user_id"] == user.id

@pytest.mark.asyncio
async def test_cartitem_create_batch():
    client = await get_client()
    user_service = UserService()
    product_service = ProductService()

    admin = await user_service.create(UserCreate(
        username="cart_items_admin_batch_create", 
        email="cart_items_admin_batch_create@example.com", 
        password="pass123", 
        is_confirmed=True, 
        is_admin=True
    ))
    user = await user_service.create(UserCreate(
        username="cart_items_user_batch_create", 
        email="cart_items_user_batch_create@example.com", 
        password="pass123", 
        is_confirmed=True
    ))
    product1 = await product_service.create(ProductCreate(
        name="cart_items_create_batch1", 
        price=10,
        description="",
        category_id=None,
        image=None
    ))
    product2 = await product_service.create(ProductCreate(
        name="cart_items_create_batch2", 
        price=20,
        description="",
        category_id=None,
        image=None
    ))

    admin_token = (await client.post("/api/auth/login", json={
        "email": admin.email, 
        "password": "pass123"
    })).json()

    user_token = (await client.post("/api/auth/login", json={
        "email": user.email, 
        "password": "pass123"
    })).json()

    data = [
        {"user_id": user.id, "product_id": product1.id, "quantity": 2},
        {"user_id": user.id, "product_id": product2.id, "quantity": 3},
    ]

    resp = await client.post("/api/cart_items/batch/", json=data, headers={
        "Authorization": f"Bearer {user_token['access_token']}"
    })
    assert resp.status_code == 200
    assert len(resp.json()) == 2

    data = [
        {"user_id": admin.id, "product_id": product1.id, "quantity": 2},
        {"user_id": admin.id, "product_id": product2.id, "quantity": 3},
    ]

    resp = await client.post("/api/cart_items/batch/", json=data, headers={
        "Authorization": f"Bearer {user_token['access_token']}"
    })
    assert resp.status_code == 403

    data = [
        {"user_id": user.id, "product_id": product1.id, "quantity": 2},
        {"user_id": user.id, "product_id": product2.id, "quantity": 3},
    ]

    resp = await client.post("/api/cart_items/batch/", json=data, headers={
        "Authorization": f"Bearer {admin_token['access_token']}"
    })
    assert resp.status_code == 200
    assert len(resp.json()) == 2

    data = [
        {"user_id": admin.id, "product_id": product1.id, "quantity": 2},
        {"user_id": admin.id, "product_id": product2.id, "quantity": 3},
    ]

    resp = await client.post("/api/cart_items/batch/", json=data, headers={
        "Authorization": f"Bearer {admin_token['access_token']}"
    })
    assert resp.status_code == 200
    assert len(resp.json()) == 2

@pytest.mark.asyncio
async def test_cartitem_update():
    client = await get_client()
    user_service = UserService()
    product_service = ProductService()
    cart_service = CartItemService()

    user = await user_service.create(UserCreate(
        username="cart_items_user_update", 
        email="cart_items_user_update@example.com", 
        password="pass123", 
        is_confirmed=True
    ))
    admin = await user_service.create(UserCreate(
        username="cart_items_admin_update", 
        email="cart_items_admin_update@example.com", 
        password="pass123", 
        is_confirmed=True, 
        is_admin=True
    ))
    product = await product_service.create(ProductCreate(
        name="cart_items_update_item", 
        price=42,
        description="",
        category_id=None,
        image=None
    ))
    user_item = await cart_service.create(CartItemCreate(user_id=user.id, product_id=product.id, quantity=1))

    user_token = (await client.post("/api/auth/login", json={
        "email": user.email, 
        "password": "pass123"
    })).json()
    admin_token = (await client.post("/api/auth/login", json={
        "email": admin.email, 
        "password": "pass123"
    })).json()

    resp = await client.put(f"/api/cart_items/{user_item.id}", json={"quantity": 10}, headers={
        "Authorization": f"Bearer {user_token['access_token']}"
    })
    assert resp.status_code == 200
    assert resp.json()["quantity"] == 10

    resp = await client.put(f"/api/cart_items/{user_item.id}", json={"quantity": 5}, headers={
        "Authorization": f"Bearer {admin_token['access_token']}"
    })
    assert resp.status_code == 200
    assert resp.json()["quantity"] == 5

@pytest.mark.asyncio
async def test_cartitem_update_batch():
    client = await get_client()
    user_service = UserService()
    product_service = ProductService()
    cart_service = CartItemService()

    admin = await user_service.create(UserCreate(
        username="cart_items_admin_batch_update", 
        email="cart_items_admin_batch_update@example.com", 
        password="pass123", 
        is_confirmed=True, 
        is_admin=True
    ))
    user = await user_service.create(UserCreate(
        username="cart_items_user_batch_update", 
        email="cart_items_user_batch_update@example.com", 
        password="pass123", 
        is_confirmed=True
    ))
    product = await product_service.create(ProductCreate(
        name="cart_items_update_batch", 
        price=33,
        description="",
        category_id=None,
        image=None
    ))

    item1 = await cart_service.create(CartItemCreate(user_id=user.id, product_id=product.id, quantity=1))
    item2 = await cart_service.create(CartItemCreate(user_id=user.id, product_id=product.id, quantity=2))

    admin_token = (await client.post("/api/auth/login", json={
        "email": admin.email, 
        "password": "pass123"
    })).json()

    update_payload = {
        "ids": [item1.id, item2.id],
        "items": [
            {"quantity": 5},
            {"quantity": 6},
        ]
    }

    resp = await client.put("/api/cart_items/batch/", json=update_payload, headers={
        "Authorization": f"Bearer {admin_token['access_token']}"
    })
    assert resp.status_code == 200
    assert len(resp.json()) == 2
    assert resp.json()[0]["quantity"] == 5 or resp.json()[1]["quantity"] == 5
    assert resp.json()[0]["quantity"] == 6 or resp.json()[1]["quantity"] == 6

@pytest.mark.asyncio
async def test_cartitem_delete():
    client = await get_client()
    user_service = UserService()
    product_service = ProductService()
    cart_service = CartItemService()

    user = await user_service.create(UserCreate(
        username="cart_items_user_delete", 
        email="cart_items_user_delete@example.com", 
        password="pass123", 
        is_confirmed=True
    ))
    admin = await user_service.create(UserCreate(
        username="cart_items_admin_delete", 
        email="cart_items_admin_delete@example.com", 
        password="pass123", 
        is_confirmed=True, 
        is_admin=True
    ))
    product = await product_service.create(ProductCreate(
        name="cart_items_delete_item", 
        price=80,
        description="",
        category_id=None,
        image=None
    ))
    item = await cart_service.create(CartItemCreate(user_id=user.id, product_id=product.id, quantity=1))

    user_token = (await client.post("/api/auth/login", json={
        "email": user.email, 
        "password": "pass123"
    })).json()
    admin_token = (await client.post("/api/auth/login", json={
        "email": admin.email, 
        "password": "pass123"
    })).json()

    other = await user_service.create(UserCreate(
        username="cart_items_other", 
        email="cart_items_other@example.com", 
        password="pass123", 
        is_confirmed=True
    ))
    other_token = (await client.post("/api/auth/login", json={
        "email": other.email, 
        "password": "pass123"
    })).json()

    resp = await client.delete(f"/api/cart_items/{item.id}", headers={
        "Authorization": f"Bearer {other_token['access_token']}"
    })
    assert resp.status_code == 403

    resp = await client.delete(f"/api/cart_items/{item.id}", headers={
        "Authorization": f"Bearer {user_token['access_token']}"
    })
    assert resp.status_code == 200
    assert resp.json()["id"] == item.id

@pytest.mark.asyncio
async def test_cartitem_delete_batch():
    client = await get_client()
    user_service = UserService()
    product_service = ProductService()
    cart_service = CartItemService()

    admin = await user_service.create(UserCreate(
        username="cart_items_admin_batch_delete", 
        email="cart_items_admin_batch_delete@example.com", 
        password="pass123", 
        is_confirmed=True, 
        is_admin=True
    ))
    user = await user_service.create(UserCreate(
        username="cart_items_user_batch_delete", 
        email="cart_items_user_batch_delete@example.com",
        password="pass123", 
        is_confirmed=True
    ))
    product = await product_service.create(ProductCreate(
        name="cart_items_delete_batch", 
        price=22,
        description="",
        category_id=None,
        image=None
    ))

    item1 = await cart_service.create(CartItemCreate(user_id=user.id, product_id=product.id, quantity=2))
    item2 = await cart_service.create(CartItemCreate(user_id=user.id, product_id=product.id, quantity=3))

    admin_token = (await client.post("/api/auth/login", json={
        "email": admin.email, 
        "password": "pass123"
    })).json()

    delete_payload = {"ids": [item1.id, item2.id]}

    resp = await client.request(
        "DELETE",
        "/api/cart_items/batch/",
        json=delete_payload,
        headers={"Authorization": f"Bearer {admin_token['access_token']}"}
    )
    assert resp.status_code == 200
    deleted_ids = [item["id"] for item in resp.json()]
    assert item1.id in deleted_ids and item2.id in deleted_ids