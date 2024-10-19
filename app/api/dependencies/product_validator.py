from sqlalchemy.orm import Session
from app.models import Product
from app.schemas.product import ProductCreate, ProductUpdate
from app.api.exceptions.GlobalException import (
    InvalidProductDataException,
    ProductAlreadyExistsException,
)


class ProductValidator:
    def __init__(self, db: Session):
        self.db = db

    def validate_unique_name(self, name: str):
        existing_product = self.db.query(Product).filter(Product.name == name).first()
        if existing_product:
            raise ProductAlreadyExistsException()

    def validate_product_data(self, product_data: ProductCreate | ProductUpdate):
        errors = []

        if product_data.price is not None:
            if (
                not isinstance(product_data.price, (float, int))
                or product_data.price < 0
            ):
                errors.append("Price must be a positive number.")

        if product_data.stock is not None:
            if not isinstance(product_data.stock, int) or product_data.stock < 0:
                errors.append("Stock must be a positive integer.")

        if errors:
            raise InvalidProductDataException(errors)
