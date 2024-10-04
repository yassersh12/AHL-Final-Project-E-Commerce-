from fastapi import FastAPI, HTTPException, APIRouter, Query
from typing import List, Optional
from decimal import Decimal
from fastapi import HTTPException
from app.models import Product
from app.api.services.product_service import ProductService

router = APIRouter()
product_service = ProductService()


@router.post("/products", response_model=Product)
def create_product(product: Product):
    return product_service.create_product(product)


@router.get("/products/{product_id}", response_model=Product)
def get_proudct(product_id: str):
    product = product_service.get_product(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product Not Found")
    return product


@router.get("/products", response_model=List[Product])
def get_all_products():
    return list(product_service.products.values())


@router.put("/products/{product_id}", response_model=Product)
def update_product(product_id: str, updated_product: Product):
    product = product_service.update_product(product_id, updated_product)
    if product is None:
        raise HTTPException(status_code=404, detail="Product Not Found")
    return product


@router.delete("/products/{product_id}")
def delete_product(product_id: str):
    product = product_service.delete_product(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="product not found ! ")
    return product
