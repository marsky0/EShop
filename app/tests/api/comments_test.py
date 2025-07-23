import pytest
from app.schemas.users import UserCreate
from app.schemas.comments import CommentCreate
from app.services.user_service import UserService
from app.services.comment_service import CommentService
from app.tests.utils import get_client


@pytest.mark.asyncio
async def test_comments_list():
    client = await get_client()
    comment_service = CommentService()

    comment = await comment_service.create(CommentCreate(user_id=None, text="comments_list_text"))

    resp = await client.get("/api/comments/")
    assert resp.status_code == 200
    assert any(c["id"] == comment.id for c in resp.json())


@pytest.mark.asyncio
async def test_comments_get_by_id():
    client = await get_client()
    comment_service = CommentService()

    comment = await comment_service.create(CommentCreate(user_id=None, text="comments_get_by_id_text"))

    resp = await client.get(f"/api/comments/{comment.id}")
    assert resp.status_code == 200
    assert resp.json()["id"] == comment.id


@pytest.mark.asyncio
async def test_comments_create():
    client = await get_client()
    user_service = UserService()

    user_data = {
        "username": "comments_user_create",
        "email": "comments_user_create@example.com",
        "password": "pass123",
        "is_confirmed": True,
    }
    admin_data = {
        "username": "comments_admin_create",
        "email": "comments_admin_create@example.com",
        "password": "pass123",
        "is_confirmed": True,
        "is_admin": True,
    }

    user = await user_service.create(UserCreate(**user_data))
    admin = await user_service.create(UserCreate(**admin_data))

    user_token = (await client.post("/api/auth/login", json={
        "email": user_data["email"], 
        "password": user_data["password"]
    })).json()
    admin_token = (await client.post("/api/auth/login", json={
        "email": admin_data["email"], 
        "password": admin_data["password"]
    })).json()

    resp = await client.post("/api/comments/", json={
        "user_id": user.id,
        "text": "text1"
    }, headers={"Authorization": f"Bearer {user_token['access_token']}"})
    assert resp.status_code == 200
    assert resp.json()["text"] == "text1"

    resp = await client.post("/api/comments/", json={
        "user_id": admin.id,
        "text": "text2"
    }, headers={"Authorization": f"Bearer {user_token['access_token']}"})
    assert resp.status_code == 403

    resp = await client.post("/api/comments/", json={
        "user_id": user.id,
        "text": "text3"
    }, headers={"Authorization": f"Bearer {admin_token['access_token']}"})
    assert resp.status_code == 200
    assert resp.json()["text"] == "text3"


@pytest.mark.asyncio
async def test_comments_update():
    client = await get_client()
    user_service = UserService()
    comment_service = CommentService()

    user = await user_service.create(UserCreate(
        username="comments_user_update",
        email="comments_user_update@example.com",
        password="pass123",
        is_confirmed=True,
    ))
    admin = await user_service.create(UserCreate(
        username="comments_admin_update",
        email="comments_admin_update@example.com",
        password="pass123",
        is_confirmed=True,
        is_admin=True,
    ))

    user_comment = await comment_service.create(CommentCreate(user_id=user.id, text="user original text"))
    admin_comment = await comment_service.create(CommentCreate(user_id=admin.id, text="admin original text"))

    user_token = (await client.post("/api/auth/login", json={
        "email": user.email,
        "password": "pass123"
    })).json()
    admin_token = (await client.post("/api/auth/login", json={
        "email": admin.email, 
        "password": "pass123"
    })).json()

    resp = await client.put(f"/api/comments/{user_comment.id}", json={"text": "updated by user"}, headers={
        "Authorization": f"Bearer {user_token['access_token']}"
    })
    assert resp.status_code == 200
    assert resp.json()["text"] == "updated by user"

    resp = await client.put(f"/api/comments/{admin_comment.id}", json={"text": "hacked"}, headers={
        "Authorization": f"Bearer {user_token['access_token']}"
    })
    assert resp.status_code == 403

    resp = await client.put(f"/api/comments/{user_comment.id}", json={"text": "updated by admin"}, headers={
        "Authorization": f"Bearer {admin_token['access_token']}"
    })
    assert resp.status_code == 200
    assert resp.json()["text"] == "updated by admin"


@pytest.mark.asyncio
async def test_comments_remove():
    client = await get_client()
    user_service = UserService()
    comment_service = CommentService()

    user = await user_service.create(UserCreate(
        username="comments_user_remove",
        email="comments_user_remove@example.com",
        password="pass123",
        is_confirmed=True,
    ))
    admin = await user_service.create(UserCreate(
        username="comments_admin_remove",
        email="comments_admin_remove@example.com",
        password="pass123",
        is_confirmed=True,
        is_admin=True,
    ))

    user_comment = await comment_service.create(CommentCreate(user_id=user.id, text="to be deleted"))
    none_comment = await comment_service.create(CommentCreate(user_id=None, text="to be deleted"))
    admin_comment = await comment_service.create(CommentCreate(user_id=admin.id, text="to be deleted"))

    user_token = (await client.post("/api/auth/login", json={
        "email": user.email, 
        "password": "pass123"
    })).json()
    admin_token = (await client.post("/api/auth/login", json={
        "email": admin.email, 
        "password": "pass123"
    })).json()

    resp = await client.delete(f"/api/comments/{user_comment.id}", headers={
        "Authorization": f"Bearer {user_token['access_token']}"
    })
    assert resp.status_code == 200
    assert resp.json()["id"] == user_comment.id

    resp = await client.delete(f"/api/comments/{admin_comment.id}", headers={
        "Authorization": f"Bearer {user_token['access_token']}"
    })
    assert resp.status_code == 403

    resp = await client.delete(f"/api/comments/{admin_comment.id}", headers={
        "Authorization": f"Bearer {admin_token['access_token']}"
    })
    assert resp.status_code == 200
    assert resp.json()["id"] == admin_comment.id

    resp = await client.delete(f"/api/comments/{none_comment.id}", headers={
        "Authorization": f"Bearer {admin_token['access_token']}"
    })
    assert resp.status_code == 200
    assert resp.json()["id"] == none_comment.id
