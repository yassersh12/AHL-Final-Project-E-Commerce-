from uuid import UUID
from app.api.exceptions.global_exceptions import InternalServerErrorException, OrderNotFoundException, OutOfStockException, ProductDoesNotExistException
from app.api.routes import status
from app.api.services.order_service import OrderService
from app.schemas.order import OrderCreationResponse, OrderProductResponse, OrderResponse
from fastapi import FastAPI, HTTPException, APIRouter
from typing import List, Optional
from fastapi.responses import JSONResponse


router = APIRouter()
order_service = OrderService()

@router.post("/orders", response_model=OrderCreationResponse)
def create_order(orderItems : List[OrderProductResponse]):
    try:
        orderResponse = order_service.create_order(order_items= orderItems)
    except Exception:
        raise InternalServerErrorException()

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=orderResponse.dict()
    )

@router.get("/orders/{order_id}", response_model=OrderResponse)
def get_order_details(order_id: UUID):
    try:
        order_details = order_service.get_order_by_id(order_id)
    except Exception:
        raise InternalServerErrorException()
    
    return order_details

@router.put("/orders/{order_id}/status", response_model=OrderResponse)
def update_order_status(order_id: UUID, status_name: str):
    # TODO: Implement admin authorization check when dependency is available
    try:
        updated_order_response = order_service.update_order_status(order_id, status_name)

    except Exception:
        raise InternalServerErrorException()
    
    #Returns 200 OK
    return updated_order_response

@router.delete("/orders/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def cancel_order(order_id: UUID):
    # TODO: Implement user authentication check when dependency is available
    try:
        order_service.cancel_order(order_id)
    except Exception as e:
        raise InternalServerErrorException()



