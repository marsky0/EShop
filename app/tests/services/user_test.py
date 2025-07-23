import pytest
from app.services.user_service import UserService
from app.schemas.users import UserCreate, UserUpdate

from app.database.db import init_db

@pytest.mark.asyncio
async def test_user_service_list():
    await init_db()
    user_service = UserService()

    user1 = await user_service.create(UserCreate(
        username="user_service_list_user1",
        email="user_service_list_user1@example.com",
        password="pass"
    ))
    user2 = await user_service.create(UserCreate(
        username="user_service_list_user2",
        email="user_service_list_user2@example.com",
        password="pass"
    ))

    users = await user_service.list()

    emails = [u.email for u in users]
    assert user1.email in emails
    assert user2.email in emails


@pytest.mark.asyncio
async def test_user_service_create():
    await init_db()
    user_service = UserService()

    data = UserCreate(
        username="user_service_create_username",
        email="user_service_create_email@example.com",
        password="user_service_create_password"
    )

    user = await user_service.create(data)

    assert user.id is not None
    assert user.username == "user_service_create_username"
    assert user.email == "user_service_create_email@example.com"


@pytest.mark.asyncio
async def test_user_service_get_by_id():
    await init_db()
    user_service = UserService()

    created = await user_service.create(UserCreate(
        username="user_service_get_by_id",
        email="user_service_get_by_id@example.com",
        password="pass"
    ))

    fetched = await user_service.get_by_id(created.id)

    assert fetched.id == created.id
    assert fetched.email == created.email


@pytest.mark.asyncio
async def test_user_service_get_by_email():
    await init_db()
    user_service = UserService()

    created = await user_service.create(UserCreate(
        username="user_service_get_by_email",
        email="user_service_get_by_email@example.com",
        password="pass"
    ))

    fetched = await user_service.get_by_email("user_service_get_by_email@example.com")

    assert fetched.id == created.id
    assert fetched.email == created.email


@pytest.mark.asyncio
async def test_user_service_get_by_username():
    await init_db()
    user_service = UserService()

    created = await user_service.create(UserCreate(
        username="user_service_get_by_username",
        email="user_service_get_by_username@example.com",
        password="pass"
    ))

    fetched = await user_service.get_by_username("user_service_get_by_username")

    assert fetched.id == created.id
    assert fetched.username == created.username


@pytest.mark.asyncio
async def test_user_service_update():
    await init_db()
    user_service = UserService()

    created = await user_service.create(UserCreate(
        username="user_service_update_username",
        email="user_service_update@example.com",
        password="pass"
    ))

    updated = await user_service.update(created.id, UserUpdate(
        username="user_service_update_updated",
        is_admin=True
    ))

    assert updated.username == "user_service_update_updated"
    assert updated.is_admin is True


@pytest.mark.asyncio
async def test_user_service_remove():
    await init_db()
    user_service = UserService()

    created = await user_service.create(UserCreate(
        username="user_service_remove_username",
        email="user_service_remove@example.com",
        password="pass"
    ))

    removed = await user_service.remove(created.id)

    assert removed.id == created.id

    with pytest.raises(Exception):
        await user_service.get_by_id(created.id)
