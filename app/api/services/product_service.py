from sqlalchemy.orm import Session
from sqlalchemy import and_, desc, asc
from app.models import Product
from app.schemas.product import ProductCreate, ProductUpdate
from app.models import ProductResponse, ProductSearchParams
from uuid import UUID
from typing import Any, Dict, Optional, List
from app.api.exceptions.GlobalException import (
    PriceValidationException,
    StockValidationException,
    ProductAlreadyExistsException,
    ProductNotFoundException,
    InvalidProductDataException,
)
from fastapi import HTTPException


class ProductService:
    def __init__(self, db: Session):
        self.db = db

    def create_product(self, product: ProductCreate) -> ProductResponse:
        if self._is_product_existing(name=product.name):
            raise ProductAlreadyExistsException()

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

    def update_product(self, product_id: str, product_data: ProductUpdate):
        product = self.db.query(Product).filter(Product.id == product_id).first()

        if not product:
            raise ProductNotFoundException(product_id)

        for key, value in product_data.dict(exclude_unset=True).items():
            setattr(product, key, value)

        self.db.commit()
        self.db.refresh(product)
        return product

    def delete_product(self, product_id: UUID) -> None:
        product = self.db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise ProductNotFoundException(product_id)
        self.db.delete(product)
        self.db.commit()

    def get_all_products(self) -> list[ProductResponse]:
        products = self.db.query(Product).all()
        return [ProductResponse.from_orm(product) for product in products]

    def _is_product_existing(self, **filters: Dict[str, Any]) -> bool:
        return self.db.query(Product).filter_by(**filters).first() is not None

    def update_model_instance(self, instance: Any, updates: Dict[str, Any]) -> None:
        for attr, value in updates.items():
            setattr(instance, attr, value)

    def search_products(self, params: ProductSearchParams) -> Dict:
        name = params.name
        min_price = params.min_price
        max_price = params.max_price
        is_available = params.isAvailable
        page = params.page
        page_size = params.page_size
        sort_by = params.sort_by
        sort_order = params.sort_order

        filtered_products = []

        for product_id, product_data in self.products_db.items():
            if name and name.lower() not in product_data["name"].lower():
                continue
            if min_price is not None and product_data["price"] < min_price:
                continue
            if max_price is not None and product_data["price"] > max_price:
                continue
            if is_available is not None and product_data["isAvailable"] != is_available:
                continue
            filtered_products.append(
                {
                    "id": product_id,
                    "name": product_data["name"],
                    "price": product_data["price"],
                    "stock": product_data["stock"],
                    "isAvailable": product_data["isAvailable"],
                    "created_at": product_data["created_at"],
                }
            )

        try:
            if sort_order == "asc":
                filtered_products.sort(key=lambda x: x[sort_by])
            elif sort_order == "desc":
                filtered_products.sort(key=lambda x: x[sort_by], reverse=True)
        except KeyError:
            raise ValueError(f"Invalid sort field: {sort_by}")

        total_products = len(filtered_products)
        total_pages = (total_products + page_size - 1) // page_size
        start = (page - 1) * page_size
        end = start + page_size
        paginated_products = filtered_products[start:end]

        return {
            "page": page,
            "total_pages": total_pages,
            "products_per_page": page_size,
            "total_products": total_products,
            "products": paginated_products,
        }
