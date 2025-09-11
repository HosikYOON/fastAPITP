import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import Base, async_engine
from fastapi.concurrency import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await async_engine.dispose()


from app.routers import user as user_router
from app.routers import product as product_router
from app.routers import review as review_router
from app.routers import cart as cart_router
from app.routers import order as order_router

app = FastAPI(lifespan=lifespan)

app.include_router(user_router.router, prefix="/users", tags=["users"])
app.include_router(product_router.router, prefix="/products", tags=["products"])
app.include_router(review_router.router, prefix="/reviews", tags=["reviews"])
app.include_router(cart_router.router, prefix="/cart", tags=["cart"])
app.include_router(order_router.router, prefix="/orders", tags=["orders"])


def main():
    print("Hello from fastapitp!")


from app.middlewares.authentication import AuthMiddleware

app.add_middleware(AuthMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8081, reload=True)
