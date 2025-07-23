import pytest
from app.services.product_service import ProductService
from app.services.category_service import CategoryService
from app.services.order_service import OrderService
from app.services.user_service import UserService
from app.schemas.products import ProductCreate, ProductUpdate
from app.schemas.categories import CategoryCreate
from app.schemas.orders import OrderCreate, OrderUpdate, OrderStatus
from app.schemas.users import UserCreate

from app.database.db import init_db

@pytest.mark.asyncio
async def test_order_service_list():
    await init_db()
    service = OrderService()
    product_service = ProductService()

    product = await product_service.create(ProductCreate(
        category_id=None,
        name="order_service_list_product",
        description="order_service_list_desc",
        price=123.45,
        image=None
    ))

    await service.create(OrderCreate(
        user_id=None,
        product_id=product.id,
        quantity=2,
        status=OrderStatus.new
    ))

    orders = await service.list()
    assert isinstance(orders, list)


@pytest.mark.asyncio
async def test_order_service_get_by_id():
    await init_db()
    service = OrderService()
    user_service = UserService()
    product_service = ProductService()

    user = await user_service.create(UserCreate(
        username="order_service_get_by_id_user",
        email="order_service_get_by_id_user@example.com",
        password="pass123",
        is_confirmed=True
    ))

    product = await product_service.create(ProductCreate(
        category_id=None,
        name="order_service_get_by_id_product",
        description="order_service_get_by_id_desc",
        price=123.45,
        image=None
    ))

    order = await service.create(OrderCreate(
        user_id=user.id,
        product_id=product.id,
        quantity=2,
        status=OrderStatus.new
    ))

    fetched = await service.get_by_id(order.id)
    assert fetched.id == order.id


@pytest.mark.asyncio
async def test_order_service_create():
    await init_db()
    service = OrderService()
    user_service = UserService()
    product_service = ProductService()

    user = await user_service.create(UserCreate(
        username="order_service_create_user",
        email="order_service_create_user@example.com",
        password="pass123",
        is_confirmed=True
    ))

    product = await product_service.create(ProductCreate(
        category_id=None,
        name="order_service_create_product",
        description="order_service_create_desc",
        price=150.0,
        image=None
    ))

    order = await service.create(OrderCreate(
        user_id=user.id,
        product_id=product.id,
        quantity=5,
        status=OrderStatus.new
    ))

    assert order.id > 0
    assert order.user_id == user.id
    assert order.product_id == product.id
    assert order.quantity == 5
    assert order.status == OrderStatus.new


@pytest.mark.asyncio
async def test_order_service_update():
    await init_db()
    service = OrderService()
    user_service = UserService()
    product_service = ProductService()

    user = await user_service.create(UserCreate(
        username="order_service_update_user",
        email="order_service_update_user@example.com",
        password="pass123",
        is_confirmed=True
    ))

    product = await product_service.create(ProductCreate(
        category_id=None,
        name="order_service_update_product",
        description="order_service_update_desc",
        price=200.0,
        image=None
    ))

    order = await service.create(OrderCreate(
        user_id=user.id,
        product_id=product.id,
        quantity=1,
        status=OrderStatus.new
    ))

    updated = await service.update(order.id, OrderUpdate(
        quantity=10,
        status=OrderStatus.paid
    ))

    assert updated.quantity == 10
    assert updated.status == OrderStatus.paid


@pytest.mark.asyncio
async def test_order_service_remove():
    await init_db()
    service = OrderService()
    user_service = UserService()
    product_service = ProductService()

    user = await user_service.create(UserCreate(
        username="order_service_remove_user",
        email="order_service_remove_user@example.com",
        password="pass123",
        is_confirmed=True
    ))

    product = await product_service.create(ProductCreate(
        category_id=None,
        name="order_service_remove_product",
        description="order_service_remove_desc",
        price=99.99,
        image=None
    ))

    order = await service.create(OrderCreate(
        user_id=user.id,
        product_id=product.id,
        quantity=3,
        status=OrderStatus.new
    ))

    removed = await service.remove(order.id)
    assert removed.id == order.id