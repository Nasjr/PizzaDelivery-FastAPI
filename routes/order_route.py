from typing import List
from fastapi import APIRouter, Depends, HTTPException,status

from database.models import Order, User
from routes.auth_route import get_current_user
from database.models import Order
from JWT.JWT_utils import verify_token
from database.database import get_db
from sqlalchemy.orm import Session
from schemas.orders_schema import OrderModel
from services.order_service import OrderService

order_router = APIRouter(
    prefix='/orders',
    tags=['orders']
)


def get_order_service(db: Session = Depends(get_db)) -> OrderService:
    return OrderService(db)


@order_router.get('/', status_code=status.HTTP_200_OK)
async def get_user_orders(
    current_user: dict = Depends(get_current_user),
    service: OrderService = Depends(get_order_service)
):
    return service.get_user_orders(current_user['userId'])

@order_router.get('/all', status_code=status.HTTP_200_OK)
async def get_all_orders(current_user: dict = Depends(get_current_user),
                          service: OrderService = Depends(get_order_service)):
    return service.get_all_orders(current_user['userId'])

@order_router.get('/{order_id}')
async def get_order_by_id(order_id: int, current_user: dict = Depends(get_current_user), service: OrderService = Depends(get_order_service)):
    return service.get_order_by_id(order_id)

@order_router.put('/update/{order_id}')
async def update_order(order_id: int, order: OrderModel, current_user: dict = Depends(get_current_user), service: OrderService = Depends(get_order_service)):
    return service.update_order(order_id, order, current_user['userId'])
            
@order_router.delete('/delete/{order_id}', status_code=status.HTTP_200_OK)
async def delete_order(order_id: int, current_user: dict = Depends(get_current_user), service: OrderService = Depends(get_order_service)):
    return service.delete_order(order_id, current_user['userId'])

@order_router.post('/new', status_code=status.HTTP_201_CREATED, response_model=OrderModel)
async def create_order(order: OrderModel, current_user: dict = Depends(get_current_user), service: OrderService = Depends(get_order_service)):
    return service.create_order(order, current_user['userId'])
    