from uuid import uuid4
from typing import Optional, Dict, List
from app.models import Product
from decimal import Decimal
from fastapi import FastAPI, HTTPException, APIRouter, Query


class ProductService:
    def __init__(self):
        self.products: Dict[str, Product] = {}

    def create_product(self, product: Product) -> Product:
        productId = str(uuid4())
        product.id = productId
        product.price = Decimal(product.price)
        self.products[productId] = product
        return product

    def get_product(self, productId: str) -> Optional[Product]:
        return self.products.get(productId)

    def get_product_by_name(self, name: str) -> Optional[Product]:
        for product in self.products.values():
            if product.name == name:
                return product
        return None

    def update_product(
        self, productId: str, updated_product: Product
    ) -> Optional[Product]:
        current_product = self.products.get(productId)
        updated_product.id = productId
        self.products[productId] = updated_product if current_product else None
        return self.products.get(productId)

    def delete_product(self, productId: str) -> Optional[Product]:
        return self.products.pop(productId, None)
