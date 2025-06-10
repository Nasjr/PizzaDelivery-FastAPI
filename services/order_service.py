from sqlalchemy.orm import Session
from database.models import Order, User
from schemas.orders_schema import OrderModel
from fastapi import HTTPException, status
from typing import List

class OrderService:
    def __init__(self, db: Session):
        self.db = db

    def get_user_orders(self, user_id: int) -> List[Order]:
        return self.db.query(Order).filter(Order.user_id == user_id).all()

    def get_all_orders(self, user_id: int) -> List[Order]:
        user = self.db.query(User).filter(User.id == user_id).first()
        if user and user.is_staff:
            return self.db.query(Order).all()
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not Staff member")

    def get_order_by_id(self, order_id: int) -> Order:
        order = self.db.query(Order).filter(Order.id == order_id).first()
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
        return order

    def update_order(self, order_id: int, order_data: OrderModel, user_id: int) -> Order:
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user or not user.is_staff:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not Staff Member")
        order = self.db.query(Order).filter(Order.id == order_id).first()
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
        order.quantity = order_data.quantity
        order.pizza_size = order_data.pizza_size
        order.order_status = order_data.order_status
        order.flavour = order_data.flavour
        self.db.commit()
        self.db.refresh(order)
        return order

    def delete_order(self, order_id: int, user_id: int):
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user or not user.is_staff:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not Staff Member")
        order = self.db.query(Order).filter(Order.id == order_id).first()
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order Not Found")
        self.db.delete(order)
        self.db.commit()
        return {'message': f"Order {order_id} deleted successfully"}

    def create_order(self, order_data: OrderModel, user_id: int) -> OrderModel:
        new_order = Order(
            quantity=order_data.quantity,
            pizza_size=order_data.pizza_size,
            flavour=order_data.flavour,
            user_id=user_id
        )
        self.db.add(new_order)
        self.db.commit()
        self.db.refresh(new_order)
      
        return OrderModel(
        id=new_order.id,
        quantity=new_order.quantity,
        pizza_size=new_order.pizza_size.value if hasattr(new_order.pizza_size, 'value') else new_order.pizza_size,
        flavour=new_order.flavour,
        order_status=new_order.order_status.value if hasattr(new_order.order_status, 'value') else new_order.order_status,
        user_id=new_order.user_id,

    )
