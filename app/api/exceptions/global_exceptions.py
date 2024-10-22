from fastapi import HTTPException, status, Request
from starlette.responses import JSONResponse
from starlette import status


class EmailAlreadyExistsException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email is already registered",
        )


class InvalidPasswordException(HTTPException):
    def __init__(self, errors: list):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"password_errors": errors},
        )


class PriceValidationException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Price must be a positive number.",
        )


class StockValidationException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Stock must be greater than zero.",
        )


class UserNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

class InvalidUUIDException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The provided user ID is not a valid UUID.",
        )

class ProductDoesNotExistException(HTTPException):
    def __init__(self, item_number: int = None):
        if item_number is not None:
            detail_message = f"Product {item_number} does not exist, enter a valid product_id"
        else:
            detail_message = "Product_id does not exist, enter a valid id"
            
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail_message,
        )

class OutOfStockException(HTTPException):
    def __init__(self, item_number: int = None):
        if item_number is not None:
            detail_message = f"Quantity for product {item_number} is higher than the stock."
        else:
            detail_message = "Quantity for the product is higher than the stock."
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail_message,
        )

class OrderNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )

class StatusNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Status not found",
        )

class InternalServerErrorException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"An unexpected error occurred."
        )


class DatabaseCommitException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while saving the product to the database.",
        )


async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An unexpected error occurred."},
    )
