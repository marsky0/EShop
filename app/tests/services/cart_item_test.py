import pytest
from app.services.cart_item_service import CartItemService
from app.schemas.cart_items import CartItemCreate, CartItemUpdate
from app.services.user_service import UserService
from app.schemas.users import UserCreate
from app.services.product_service import ProductService
from app.schemas.products import ProductCreate

from app.database.db import init_db


@pytest.mark.asyncio
async def test_cart_items_service_list():
    await init_db()
    service = CartItemService()
    user_service = UserService()
    product_service = ProductService()

    user = await user_service.create(UserCreate(
        username="cart_items_service_list_user",
        email="cart_items_service_list_user@example.com",
        password="pass123",
        is_confirmed=True
    ))
    product = await product_service.create(ProductCreate(
        name="cart_items_service_list_product",
        description="cart_items_service_list_product_desc",
        price=111,
        category_id=None,
        image=None
    ))
    item = await service.create(CartItemCreate(
        user_id=user.id,
        product_id=product.id,
        quantity=5
    ))

    result = await service.list()
    assert isinstance(result, list)

@pytest.mark.asyncio
async def test_cart_items_service_get_by_id():
    await init_db()
    service = CartItemService()
    user_service = UserService()
    product_service = ProductService()

    user = await user_service.create(UserCreate(
        username="cart_items_service_get_by_id_user",
        email="cart_items_service_get_by_id_user@example.com",
        password="pass123",
        is_confirmed=True
    ))
    product = await product_service.create(ProductCreate(
        name="cart_items_service_get_by_id_product",
        description="cart_items_service_get_by_id_product_desc",
        price=111,
        category_id=None,
        image=None
    ))

    item = await service.create(CartItemCreate(
        user_id=user.id,
        product_id=product.id,
        quantity=5
    ))

    result = await service.get_by_id(item.id)
    assert result.id == item.id


@pytest.mark.asyncio
async def test_cart_items_service_get_by_user_id():
    await init_db()
    service = CartItemService()
    user_service = UserService()
    product_service = ProductService()

    user = await user_service.create(UserCreate(
        username="cart_items_service_get_by_user_id_user",
        email="cart_items_service_get_by_user_id_user@example.com",
        password="pass123",
        is_confirmed=True
    ))
    product = await product_service.create(ProductCreate(
        name="cart_items_service_get_by_user_id_product",
        description="cart_items_service_get_by_user_id_product_desc",
        price=111,
        category_id=None,
        image=None
    ))

    await service.create(CartItemCreate(
        user_id=user.id,
        product_id=product.id,
        quantity=1
    ))
    await service.create(CartItemCreate(
        user_id=user.id,
        product_id=product.id,
        quantity=2
    ))

    items = await service.get_by_user_id(user.id)
    assert all(item.user_id == user.id for item in items)


@pytest.mark.asyncio
async def test_cart_items_service_create():
    await init_db()
    service = CartItemService()
    user_service = UserService()
    product_service = ProductService()

    user = await user_service.create(UserCreate(
        username="cart_items_service_create_user",
        email="cart_items_service_create_user@example.com",
        password="pass123",
        is_confirmed=True
    ))
    product = await product_service.create(ProductCreate(
        name="cart_items_service_create_product",
        description="cart_items_service_create_product_desc",
        price=111,
        category_id=None,
        image=None
    ))

    item = await service.create(CartItemCreate(
        user_id=user.id,
        product_id=product.id,
        quantity=3
    ))

    assert item.id > 0
    assert item.user_id == user.id
    assert item.product_id == product.id
    assert item.quantity == 3


@pytest.mark.asyncio
async def test_cart_items_service_update():
    await init_db()
    service = CartItemService()
    user_service = UserService()
    product_service = ProductService()

    user = await user_service.create(UserCreate(
        username="cart_items_service_update_user",
        email="cart_items_service_update_user@example.com",
        password="pass123",
        is_confirmed=True
    ))
    product = await product_service.create(ProductCreate(
        name="cart_items_service_update_product",
        description="cart_items_service_update_product_desc",
        price=111,
        category_id=None,
        image=None
    ))

    item = await service.create(CartItemCreate(
        user_id=user.id,
        product_id=product.id,
        quantity=7
    ))

    updated = await service.update(item.id, CartItemUpdate(quantity=99))
    assert updated.quantity == 99


@pytest.mark.asyncio
async def test_cart_items_service_remove():
    await init_db()
    service = CartItemService()
    user_service = UserService()
    product_service = ProductService()

    user = await user_service.create(UserCreate(
        username="cart_items_service_remove_user",
        email="cart_items_service_remove_user@example.com",
        password="pass123",
        is_confirmed=True
    ))
    product = await product_service.create(ProductCreate(
        name="cart_items_service_remove_product",
        description="cart_items_service_remove_product_desc",
        price=111,
        category_id=None,
        image=None
    ))

    item = await service.create(CartItemCreate(
        user_id=user.id,
        product_id=product.id,
        quantity=2
    ))

    removed = await service.remove(item.id)
    assert removed.id == item.id

    with pytest.raises(Exception):
        await service.get_by_id(item.id)


@pytest.mark.asyncio
async def test_cart_items_service_create_batch():
    await init_db()
    service = CartItemService()
    user_service = UserService()
    product_service = ProductService()

    user = await user_service.create(UserCreate(
        username="cart_items_service_create_batch_user",
        email="cart_items_service_create_batch_user@example.com",
        password="pass123",
        is_confirmed=True
    ))
    product = await product_service.create(ProductCreate(
        name="cart_items_service_create_batch_product",
        description="cart_items_service_create_batch_product_desc",
        price=111,
        category_id=None,
        image=None
    ))

    batch = await service.create_batch([
        CartItemCreate(
            user_id=user.id,
            product_id=product.id,
            quantity=3
        ),
        CartItemCreate(
            user_id=user.id,
            product_id=product.id,
            quantity=4
        )
    ])

    assert len(batch) == 2
    assert batch[0].quantity == 3
    assert batch[1].quantity == 4


@pytest.mark.asyncio
async def test_cart_items_service_update_batch():
    await init_db()
    service = CartItemService()
    user_service = UserService()
    product_service = ProductService()

    user = await user_service.create(UserCreate(
        username="cart_items_service_update_batch_user",
        email="cart_items_service_update_batch_user@example.com",
        password="pass123",
        is_confirmed=True
    ))
    product = await product_service.create(ProductCreate(
        name="cart_items_service_update_batch_product",
        description="cart_items_service_update_batch_product_desc",
        price=111,
        category_id=None,
        image=None
    ))

    created = await service.create_batch([
        CartItemCreate(
            user_id=user.id,
            product_id=product.id,
            quantity=10
        ),
        CartItemCreate(
            user_id=user.id,
            product_id=product.id,
            quantity=20
        )
    ])
    ids = [item.id for item in created]

    updated = await service.update_batch(ids, [
        CartItemUpdate(quantity=30),
        CartItemUpdate(quantity=40)
    ])

    assert updated[0].quantity == 30
    assert updated[1].quantity == 40


@pytest.mark.asyncio
async def test_cart_items_service_remove_batch():
    await init_db()
    service = CartItemService()
    user_service = UserService()
    product_service = ProductService()

    user = await user_service.create(UserCreate(
        username="cart_items_service_remove_batch_user",
        email="cart_items_service_remove_batch_user@example.com",
        password="pass123",
        is_confirmed=True
    ))
    product = await product_service.create(ProductCreate(
        name="cart_items_service_remove_batch_product",
        description="cart_items_service_remove_batch_product_desc",
        price=111,
        category_id=None,
        image=None
    ))

    created = await service.create_batch([
        CartItemCreate(
            user_id=user.id,
            product_id=product.id,
            quantity=6
        ),
        CartItemCreate(
            user_id=user.id,
            product_id=product.id,
            quantity=7
        )
    ])
    ids = [item.id for item in created]

    removed = await service.remove_batch(ids)
    assert len(removed) == 2
    assert {r.id for r in removed} == set(ids)

    for id in ids:
        with pytest.raises(Exception):
            await service.get_by_id(id)
