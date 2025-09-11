from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.database import get_db
from app.schemas.product import ProductRead, ProductCreate
from app.services.product_service import ProductService

router = APIRouter()


async def get_product_service(db: AsyncSession = Depends(get_db)) -> ProductService:
    return ProductService(db)


@router.post("/", response_model=ProductRead)
async def create_product(
    product: ProductCreate, product_service: ProductService = Depends(get_product_service)
):
    return await product_service.create_product(product=product)


@router.get("/", response_model=List[ProductRead])
async def read_products(
    skip: int = 0, limit: int = 100, product_service: ProductService = Depends(get_product_service)
):
    products = await product_service.get_products(skip=skip, limit=limit)
    return products


@router.get("/{product_id}", response_model=ProductRead)
async def read_product(
    product_id: int, product_service: ProductService = Depends(get_product_service)
):
    db_product = await product_service.get_product(product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


@router.put("/{product_id}", response_model=ProductRead)
async def update_product(
    product_id: int, product: ProductCreate, product_service: ProductService = Depends(get_product_service)
):
    db_product = await product_service.update_product(
        product_id=product_id, product_update=product
    )
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


@router.delete("/{product_id}", response_model=ProductRead)
async def delete_product(
    product_id: int, product_service: ProductService = Depends(get_product_service)
):
    db_product = await product_service.delete_product(product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product
