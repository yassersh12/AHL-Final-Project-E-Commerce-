from app.api.exceptions.global_exceptions import InternalServerErrorException, StatusAlreadyExistsException, StatusNameInvalidException
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
