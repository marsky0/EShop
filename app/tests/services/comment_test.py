import pytest
from app.services.comment_service import CommentService
from app.services.user_service import UserService
from app.schemas.comments import CommentCreate, CommentUpdate
from app.schemas.users import UserCreate

from app.database.db import init_db


@pytest.mark.asyncio
async def test_comment_service_list():
    await init_db()
    comment_service = CommentService()
    user_service = UserService()

    user = await user_service.create(UserCreate(
        username="comment_service_list_user",
        email="comment_service_list@example.com",
        password="123"
    ))
    comment = await comment_service.create(
        CommentCreate(user_id=user.id, text="comment_service_list_text")
    )
    comments = await comment_service.list()
    assert isinstance(comments, list)


@pytest.mark.asyncio
async def test_comment_service_get_by_id():
    await init_db()
    comment_service = CommentService()
    user_service = UserService()

    user = await user_service.create(UserCreate(
        username="comment_service_get_by_id_user",
        email="comment_service_get_by_id@example.com",
        password="123"
    ))
    comment = await comment_service.create(
        CommentCreate(user_id=user.id, text="comment_service_get_by_id_text")
    )
    fetched = await comment_service.get_by_id(comment.id)
    assert fetched.text == comment.text


@pytest.mark.asyncio
async def test_comment_service_create():
    await init_db()
    comment_service = CommentService()
    user_service = UserService()

    user = await user_service.create(UserCreate(
        username="comment_service_create_user",
        email="comment_service_create@example.com",
        password="123"
    ))
    comment = await comment_service.create(
        CommentCreate(user_id=user.id, text="comment_service_create_text")
    )
    assert comment.text == "comment_service_create_text"


@pytest.mark.asyncio
async def test_comment_service_update():
    await init_db()
    comment_service = CommentService()
    user_service = UserService()

    user = await user_service.create(UserCreate(
        username="comment_service_update_user",
        email="comment_service_update@example.com",
        password="123"
    ))
    comment = await comment_service.create(
        CommentCreate(user_id=user.id, text="initial")
    )
    updated = await comment_service.update(
        comment.id, CommentUpdate(text="comment_service_update_text")
    )
    assert updated.text == "comment_service_update_text"


@pytest.mark.asyncio
async def test_comment_service_remove():
    await init_db()
    comment_service = CommentService()
    user_service = UserService()

    user = await user_service.create(UserCreate(
        username="comment_service_remove_user",
        email="comment_service_remove@example.com",
        password="123"
    ))
    comment = await comment_service.create(
        CommentCreate(user_id=user.id, text="comment_service_remove_text")
    )
    deleted = await comment_service.remove(comment.id)
    assert deleted.id == comment.id