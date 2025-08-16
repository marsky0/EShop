from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi_limiter import FastAPILimiter
from contextlib import asynccontextmanager
import asyncio

from app.api import auth, cart_items, categories, comments, orders, products, users
from app.database.db import init_db
from app.database.redis_client import init_redis, get_redis_client

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    await init_redis()
    await FastAPILimiter.init(get_redis_client())
    yield

app = FastAPI(lifespan=lifespan)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def catch_exception_middleware(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=jsonable_encoder({"details": str(e)}))

app.middleware('http')(catch_exception_middleware)

app.include_router(auth.router)
app.include_router(cart_items.router)
app.include_router(categories.router)
app.include_router(comments.router)
app.include_router(orders.router)
app.include_router(products.router)
app.include_router(users.router)

@app.get("/")
async def root():
    return {
        "message": "Welcome to EShop API!",
        "description": "E-commerce backend built with FastAPI",
        "status": "running",
        "docs": "/docs",
        "redoc": "/redoc",
        "endpoints": {
            "auth": "/api/auth",
            "products": "/api/products", 
            "categories": "/api/categories",
            "users": "/api/users",
            "cart": "/api/cart_items",
            "orders": "/api/orders",
            "comments": "/api/comments"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
