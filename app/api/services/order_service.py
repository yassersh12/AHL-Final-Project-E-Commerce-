from datetime import datetime
from uuid import uuid4, UUID
from typing import Optional, List
from app.api.exceptions.global_exceptions import OrderNotFoundException, ProductDoesNotExistException, OutOfStockException, StatusNotFoundException
from app.api.services.order_status_service import OrderStatusService
from app.api.services.product_service import ProductService 
from app.models import Order, OrderProduct
from decimal import Decimal
from app.schemas.order import OrderCreationResponse, OrderItem, OrderResponse
from fastapi import FastAPI, HTTPException, APIRouter, Query
from sqlalchemy.orm import Session


product_service = ProductService()
order_status_service = OrderStatusService()

class OrderService:
    def __init__(self, db: Session):
        self.db = db
  
    def create_order(self, order_items: List[OrderItem], user_id: Optional[UUID] = None) -> OrderCreationResponse:
        total_price = Decimal(0)
        
        for index, item in enumerate(order_items):
            product = self.product_service.get_product(item.product_id)
            if product is None:
                raise ProductDoesNotExistException(index + 1)
            elif item.quantity > product.stock:
                raise OutOfStockException(index + 1)

            total_price += product.price * item.quantity
        
        status_id = order_status_service.get_order_status_by_name("pending").id
        order_id = uuid4()
        order = Order(
            id=order_id,
            user_id=user_id,
            total_price=total_price,
            status_id=status_id
        )
        
        self.db.add(order)
        
        for item in order_items:
            order_product = OrderProduct(order_id=order_id, product_id=item.product_id, quantity=item.quantity)
            self.db.add(order_product)
        
        self.db.commit()

        orderResponse = OrderCreationResponse(
            id=order.id,
            user_id=user_id,
            total_price=total_price,
            status_id=status_id
        )
        return orderResponse


    def get_order_by_id(self, order_id: UUID) -> OrderResponse:

        order = self.db.query(Order).filter(Order.id == order_id).first()
        if not order:
            raise OrderNotFoundException()

        order_products = self.db.query(OrderProduct).filter(OrderProduct.order_id == order_id).all()

        product_responses = []
        for item in order_products:
            product_response = OrderItem(
                product_id=item.product_id,
                quantity=item.quantity
            )
            product_responses.append(product_response)

        status_name = order_status_service.get_order_status_by_id(order.status_id).name

        return OrderResponse(
            id=order.id,
            user_id=order.user_id,
            status=status_name,
            total_price=order.total_price,
            created_at=order.created_at,
            updated_at=order.updated_at,
            products=product_responses
        )

     
    def update_order_status(self, order_id: UUID, status_name: str) -> OrderResponse:

        order = self.db.query(Order).filter(Order.id == order_id).first()
        if not order:
            raise OrderNotFoundException()

        status = order_status_service.get_order_status_by_name(status_name)
        if not status:
            raise StatusNotFoundException()
        
        order.status_id = status.id
        order.updated_at = datetime.now()
        
        self.db.commit()

        return OrderResponse(
            id=order.id,
            user_id=order.user_id,
            status=status.id,
            total_price=order.total_price,
            created_at=order.created_at,
            updated_at=order.updated_at
        )

    
    def cancel_order(self, order_id: UUID) -> None:
        order = self.db.query(Order).filter(Order.id == order_id).first()
        status = order_status_service.get_order_status_by_name('pending')
        
        if not order:
            raise OrderNotFoundException()
        elif order.status_id != status.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only pending orders can be canceled."
            )

        canceled_status = order_status_service.get_order_status_by_name('canceled')
        order.status_id = canceled_status.id
        order.updated_at = datetime.now()

        self.db.commit()

