from typing import List
from app.api.exceptions.global_exceptions import StatusAlreadyExistsException, StatusNotFoundException
from app.models import OrderStatus

class OrderStatusService:
    def __init__(self):
        self.order_statuses: List[OrderStatus] = []

    def create_order_status(self, name: str) -> OrderStatus:
        if any(status.name == name for status in self.order_statuses):
            raise StatusAlreadyExistsException()

        new_status = OrderStatus(name=name)
        self.order_statuses.append(new_status)
        return new_status

    def get_order_status_by_name(self, name: str) -> OrderStatus:
        for status in self.order_statuses:
            if status.name == name:
                return status
        raise StatusNotFoundException()
