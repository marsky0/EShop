import pytest
from app.services.product_service import ProductService 
from app.services.category_service import CategoryService
from app.schemas.products import ProductCreate, ProductUpdate
from app.schemas.categories import CategoryCreate

from app.database.db import init_db

@pytest.mark.asyncio
async def test_product_service_list():
    await init_db()
    product_service = ProductService()
    product = await product_service.create(ProductCreate(
        category_id=None,
        name="product_service_list_product",
        description="product_service_list_description",
        price=100.0,
        image=None
    ))

    products = await product_service.list()
    assert isinstance(products, list)


@pytest.mark.asyncio
async def test_product_service_get_by_id():
    await init_db()
    product_service = ProductService()
    category_service = CategoryService()

    category = await category_service.create(
        CategoryCreate(name="product_service_get_by_id_category")
    )
    product = await product_service.create(
        ProductCreate(
            category_id=category.id,
            name="product_service_get_by_id_product",
            description="product_service_get_by_id_description",
            price=100.0,
            image=None
        )
    )
    fetched = await product_service.get_by_id(product.id)
    assert fetched.name == product.name

@pytest.mark.asyncio
async def test_product_service_create():
    await init_db()
    product_service = ProductService()
    category_service = CategoryService()

    category = await category_service.create(
        CategoryCreate(name="product_service_create_category")
    )
    product = await product_service.create(
        ProductCreate(
            category_id=category.id,
            name="product_service_create_product",
            description="product_service_create_description",
            price=200.0,
            image=None
        )
    )
    assert product.name == "product_service_create_product"


@pytest.mark.asyncio
async def test_product_service_update():
    await init_db()
    product_service = ProductService()
    category_service = CategoryService()

    category = await category_service.create(
        CategoryCreate(name="product_service_update_category")
    )
    product = await product_service.create(
        ProductCreate(
            category_id=category.id,
            name="product_service_update_initial",
            description="init",
            price=50.0,
            image=None
        )
    )
    updated = await product_service.update(
        product.id,
        ProductUpdate(name="product_service_update_name")
    )
    assert updated.name == "product_service_update_name"


@pytest.mark.asyncio
async def test_product_service_remove():
    await init_db()
    product_service = ProductService()
    category_service = CategoryService()

    category = await category_service.create(
        CategoryCreate(name="product_service_remove_category")
    )
    product = await product_service.create(
        ProductCreate(
            category_id=category.id,
            name="product_service_remove_product",
            description="to remove",
            price=150.0,
            image=None
        )
    )
    deleted = await product_service.remove(product.id)
    assert deleted.id == product.id