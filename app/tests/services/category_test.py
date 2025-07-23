import pytest
from app.services.category_service import CategoryService
from app.schemas.categories import CategoryCreate, CategoryUpdate
from app.database.db import init_db


@pytest.mark.asyncio
async def test_category_service_list():
    await init_db()
    service = CategoryService()
    category_1 = await service.create(data=CategoryCreate(name="category_service_list_1"))
    category_2 = await service.create(data=CategoryCreate(name="category_service_list_2"))

    categories = await service.list()
    assert any(c.id == category_1.id for c in categories)
    assert any(c.id == category_2.id for c in categories)


@pytest.mark.asyncio
async def test_category_service_get_by_id():
    await init_db()
    service = CategoryService()
    category = await service.create(data=CategoryCreate(name="category_service_get_by_id"))

    result = await service.get_by_id(id=category.id)
    assert result.id == category.id
    assert result.name == "category_service_get_by_id"


@pytest.mark.asyncio
async def test_category_service_create():
    await init_db()
    service = CategoryService()
    category = await service.create(data=CategoryCreate(name="category_service_create"))

    assert category.id is not None
    assert category.name == "category_service_create"

@pytest.mark.asyncio
async def test_category_service_update():
    await init_db()
    service = CategoryService()
    category = await service.create(data=CategoryCreate(name="category_service_update_before"))

    updated = await service.update(id=category.id, data=CategoryUpdate(name="category_service_update_after"))
    assert updated.name == "category_service_update_after"

@pytest.mark.asyncio
async def test_category_service_remove():
    await init_db()
    service = CategoryService()
    category = await service.create(data=CategoryCreate(name="category_service_remove"))

    deleted = await service.remove(id=category.id)
    assert deleted.id == category.id