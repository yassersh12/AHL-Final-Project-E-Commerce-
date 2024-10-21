import datetime
from typing import List
from uuid import UUID
from app.api.exceptions.global_exceptions import StatusAlreadyExistsException, StatusInUseException, StatusNotFoundException
from app.models import OrderStatus
from sqlalchemy.orm import Session


class OrderStatusService:
    def __init__(self, db : Session):
        self.db = db

    def create_order_status(self, name: str) -> OrderStatus:
        if self.db.query(OrderStatus).filter(OrderStatus.name == name).first():
            raise StatusAlreadyExistsException()

        new_status = OrderStatus(name=name)
        self.db.add(new_status)
        self.db.commit()
        self.db.refresh(new_status)
        
        return new_status

    def get_order_status_by_name(self, name: str) -> OrderStatus:
        status = self.db.query(OrderStatus).filter(OrderStatus.name == name).first()
        if status :
            return status
        
        raise StatusNotFoundException()
    
    def get_order_status_by_id(self, status_id: UUID) -> OrderStatus:
        status = self.db.query(OrderStatus).filter(OrderStatus.id == status_id).first()
        if status :
            return status
        
        raise StatusNotFoundException()
    
    def update_order_status(self, status_id: UUID, name: str) -> OrderStatus:
        if any(status.name == name for status in self.order_statuses):
            raise StatusAlreadyExistsException()

        for status in self.order_statuses:
            if status.id == status_id:
                status.name = name
                status.updated_at = datetime.now()
                return status
        
        raise StatusNotFoundException()
    
    def is_status_in_use(self, status_id: UUID) -> bool:
        return any(order.status_id == status_id for order in self.orders)

    def remove_order_status(self, status_id: UUID):
        status_to_remove = self.get_order_status_by_id(status_id)
        
        if self.is_status_in_use(status_id):
            raise StatusInUseException()

        self.order_statuses = [status for status in self.order_statuses if status.id != status_id]
