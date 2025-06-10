from database.database import Base
from sqlalchemy import Column,Integer,Boolean,Text,String,ForeignKey
from sqlalchemy_utils.types import ChoiceType
from sqlalchemy.orm import relationship



class User(Base):
    __tablename__='user'
    id = Column(Integer,primary_key=True)
    name = Column(String(25),unique=True)
    email= Column(String(40),unique=True)
    password= Column(Text,nullable=True)
    is_active= Column(Boolean,default=False)
    is_staff= Column(Boolean,default=False)
    orders=relationship('Order',back_populates='user')
    def __repr__(self):
        return f"User{self.name}"


class Order(Base):
    
    __tablename__='orders'
    ORDER_STATUESES = (('PENDING','pending'),('IN-TRANSIT','in-transit'),('DELIVERED','delivered'),)
    PIZZA_SIZES = (('SMALL','small'),('LARGE','large'),('MEDIUM','medium'),('EXTRA-LARGE','extra-large'))
    id = Column(Integer,primary_key=True)
    user_id = Column(Integer,ForeignKey('user.id'),nullable=False)
    quantity = Column(Integer,nullable=False)
    order_status = Column(ChoiceType(choices=ORDER_STATUESES),default="PENDING")
    pizza_size = Column(ChoiceType(choices=PIZZA_SIZES),default="SMALL")
    flavour = Column(String)
    user = relationship('User',back_populates='orders')
    def __repr__(self):
        return f'Order{self.id}'
    
