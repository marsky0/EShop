from httpx import AsyncClient, ASGITransport

from app.database.db import get_session as get_session_sql
from main import app


async def get_client():
    async with app.router.lifespan_context(app):
        transport = ASGITransport(app=app)
        client = AsyncClient(transport=transport, base_url="http://127.0.0.1")
        return client

async def get_session():
    return await anext(get_session_sql())