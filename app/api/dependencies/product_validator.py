from sqlalchemy.orm import Session
from app.models import Product
from app.schemas.product import ProductCreate, ProductUpdate
from app.api.exceptions.global_exceptions import (
    InvalidProductDataException,
    ProductAlreadyExistsException,
    PriceValidationException,
    StockValidationException,
)


class ProductValidator:
    def __init__(self, db: Session):
        self.db = db

    def validate_unique_name(self, name: str):
        existing_product = self.db.query(Product).filter(Product.name == name).first()
        if existing_product:
            raise ProductAlreadyExistsException()
