from fastapi import APIRouter, Depends, HTTPException, status, Response, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate
from app.api.services.product_service import ProductService
from app.api.exceptions.GlobalException import (
    ProductNotFoundException,
    ProductAlreadyExistsException,
    InvalidProductDataException,
)
from app.api.dependencies.ProductValidator import ProductValidator
from uuid import UUID
from app.models import Product, ProductSearchParams
from typing import Optional, List
from decimal import Decimal
from sqlalchemy import asc, desc

router = APIRouter()


@router.post(
    "/products/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED
)
def create_product(product_data: ProductCreate, db: Session = Depends(get_db)):
    validator = ProductValidator(db)

    try:
        validator.validate_unique_name(product_data.name)
        validator.validate_product_data(product_data)

        new_product = Product(**product_data.dict())

        db.add(new_product)
        db.commit()
        db.refresh(new_product)

        return new_product
    except InvalidProductDataException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.detail)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: UUID, db: Session = Depends(get_db)):
    service = ProductService(db)
    try:
        return service.get_product_by_id(product_id)
    except ProductNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.put("/products/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: UUID, product_data: ProductUpdate, db: Session = Depends(get_db)
):
    validator = ProductValidator(db)
    service = ProductService(db)

    try:
        existing_product = service.get_product_by_id(product_id)
        if not existing_product:
            raise ProductNotFoundException(product_id)

        if product_data.name and product_data.name != existing_product.name:
            validator.validate_unique_name(product_data.name)

        validator.validate_product_data(product_data)

        updated_product = service.update_product(product_id, product_data)

        return updated_product
    except ProductNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except InvalidProductDataException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.detail)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: UUID, response: Response, db: Session = Depends(get_db)):
    service = ProductService(db)
    try:
        service.delete_product(product_id)
        response.status_code = status.HTTP_204_NO_CONTENT
    except ProductNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.get("/products", response_model=list[ProductResponse])
def get_all_products(db: Session = Depends(get_db)):
    service = ProductService(db)
    return service.get_all_products()


@router.get("/products/buy/search", response_model=List[ProductResponse])
def search_products(
    name: str = Query(None, description="Name of the product to search for"),
    min_price: float = Query(None, description="Minimum price search"),
    max_price: float = Query(None, description="Maximum price search"),
    is_available: bool = Query(None, description="Availability status search"),
    db: Session = Depends(get_db),
):
    query = db.query(Product)

    if name:
        query = query.filter(Product.name.ilike(f"%{name}%"))
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)
    if is_available is not None:
        query = query.filter(Product.is_available == is_available)

    products = query.all()

    if not products:
        raise HTTPException(
            status_code=404,
            detail="No products found in the database ->  matching the criteria",
        )

    return [ProductResponse.from_orm(product) for product in products]
