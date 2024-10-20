from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.product import (
    ProductCreate,
    ProductResponse,
    ProductUpdate,
    ProductSearchParams,
)
from fastapi import HTTPException, status, Query, Depends
from app.api.services.product_service import ProductService
from uuid import UUID
from typing import List, Optional, Dict
from app.api.exceptions.global_exceptions import (
    ProductAlreadyExistsException,
    PriceValidationException,
    ProductNotFoundException,
    StockValidationException,
    InvalidUUIDException,
    InvalidProductDataException,
    ProductValidationException,
)
from app.api.dependencies.product_validator import ProductValidator
from app.models import Product

router = APIRouter()


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(product_data: ProductCreate, db: Session = Depends(get_db)):
    service = ProductService(db)

    if service._is_product_existing(name=product_data.name):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Product already exists."
        )

    new_product = Product(**product_data.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: str,
    db: Session = Depends(get_db),
):

    try:
        product_id = UUID(product_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid UUID!"
        )

    service = ProductService(db)
    try:
        return service.get_product_by_id(product_id)
    except ProductNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found."
        )


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: UUID, db: Session = Depends(get_db)):
    service = ProductService(db)
    try:
        service.delete_product(product_id)
        return
    except ProductNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found."
        )
    except InvalidUUIDException:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid UUID!"
        )


@router.get("/", response_model=Dict)
def search_products(
    name: Optional[str] = Query(None, description="Filter by product name"),
    min_price: Optional[float] = Query(None, description="Filter by minimum price"),
    max_price: Optional[float] = Query(None, description="Filter by maximum price"),
    isAvailable: Optional[bool] = Query(None, description="Filter by availability"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Products per page"),
    sort_by: str = Query("name", description="Sort by field"),
    sort_order: str = Query("asc", description="Sort order: asc or desc"),
    db: Session = Depends(get_db),
):
    service = ProductService(db)
    try:
        params = ProductSearchParams(
            name=name,
            min_price=min_price,
            max_price=max_price,
            isAvailable=isAvailable,
            page=page,
            page_size=page_size,
            sort_by=sort_by,
            sort_order=sort_order,
        )
        return service.search_products(params)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred.",
        )
