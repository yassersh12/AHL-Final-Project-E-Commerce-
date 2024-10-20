from uuid import UUID
from app.api.exceptions.global_exceptions import InternalServerErrorException, StatusAlreadyExistsException, StatusNameInvalidException, StatusNotFoundException
from app.api.services.order_status_service import OrderStatusService
from fastapi import APIRouter, HTTPException, status

router = APIRouter()
order_status_service = OrderStatusService

@router.post("/statuses/", status_code=status.HTTP_201_CREATED)
def create_order_status(name: str):
    if not name or not isinstance(name, str):
        raise StatusNameInvalidException()

    try:
        new_status = order_status_service.create_order_status(name=name)
    except StatusAlreadyExistsException as e:
        raise e
    except Exception:
        raise InternalServerErrorException()

    return new_status

@router.get("/statuses/{status_id}", status_code=status.HTTP_200_OK)
def get_order_status_by_id(status_id: UUID):
    try:
        order_status = order_status_service.get_order_status_by_id(status_id=status_id)
    except StatusNotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Status not found")
    except Exception:
        raise InternalServerErrorException()

    return order_status
