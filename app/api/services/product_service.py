from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, asc, desc
from app.models import Product
from app.schemas.product import (
    ProductCreate,
    ProductUpdate,
    ProductSearchParams,
    ProductResponse,
)
from uuid import UUID
from typing import Any, Dict, List
from fastapi import HTTPException
from app.api.exceptions.global_exceptions import (
    ProductAlreadyExistsException,
    ProductNotFoundException,
    PriceValidationException,
    InvalidUUIDException,
    StockValidationException,
    InvalidPasswordException,
)
from pydantic import BaseModel, validator


class ProductService:
    def __init__(self, db: Session):
        self.db = db

    def create_product(self, product: ProductCreate) -> ProductResponse:
        self.validator.validate_unique_name(product.name)
        new_product = Product(**product.dict())
        self.db.add(new_product)
        self.db.commit()
        self.db.refresh(new_product)
        return ProductResponse.from_orm(new_product)

    def get_product_by_id(self, product_id: UUID) -> ProductResponse:
        product = self.db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise ProductNotFoundException(product_id)
        return ProductResponse.from_orm(product)

    def update_product(
        self, product_id: UUID, product_data: ProductUpdate
    ) -> ProductResponse:
        product = self.db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise ProductNotFoundException(product_id)

        for key, value in product_data.dict(exclude_unset=True).items():
            setattr(product, key, value)

        self.db.commit()
        self.db.refresh(product)
        return ProductResponse.from_orm(product)

    def delete_product(self, product_id: UUID) -> None:
        try:
            product_id = UUID(str(product_id))
        except ValueError:
            raise InvalidUUIDException(f"Invalid UUID: {product_id}")

        product = self.db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise ProductNotFoundException(product_id)

        self.db.delete(product)
        self.db.commit()

    def _is_product_existing(self, **filters: Dict[str, Any]) -> bool:
        return self.db.query(Product).filter_by(**filters).first() is not None

    def search_products(self, params: ProductSearchParams) -> Dict:
        query = self.db.query(Product)

        if params.name:
            query = query.filter(Product.name.ilike(f"%{params.name}%"))
        if params.min_price is not None:
            query = query.filter(Product.price >= params.min_price)
        if params.max_price is not None:
            query = query.filter(Product.price <= params.max_price)
        if params.isAvailable is not None:
            query = query.filter(Product.is_available == params.isAvailable)

        sort_column = getattr(Product, params.sort_by, None)
        if not sort_column:
            raise HTTPException(status_code=400, detail="Invalid sort field.")
        query = query.order_by(
            asc(sort_column) if params.sort_order == "asc" else desc(sort_column)
        )

        total_products = query.count()
        total_pages = (total_products + params.page_size - 1) // params.page_size
        products = (
            query.offset((params.page - 1) * params.page_size)
            .limit(params.page_size)
            .all()
        )

        return {
            "page": params.page,
            "total_pages ": total_pages,
            "products_per_page": params.page_size,
            "total_products": total_products,
            "products": [ProductResponse.from_orm(product) for product in products],
        }

    def _validate_uuid(self, product_id: str) -> None:
        try:
            UUID(product_id)
        except (ValueError, TypeError):
            raise InvalidUUIDException()
