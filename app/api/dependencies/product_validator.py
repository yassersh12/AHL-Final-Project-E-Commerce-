from sqlalchemy.orm import Session
from app.models import Product
from app.api.exceptions.global_exceptions import (
    ProductAlreadyExistsException,
)


class ProductValidator:
    def __init__(self, db: Session):
        self.db = db

    def validate_unique_name(self, name: str):
        existing_product = self.db.query(Product).filter(Product.name == name).first()
        if existing_product:
            raise ProductAlreadyExistsException()
