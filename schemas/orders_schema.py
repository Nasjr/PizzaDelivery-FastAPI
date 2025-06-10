from typing import Optional
from pydantic import BaseModel

class OrderModel(BaseModel):
    id : Optional[int]
    user_id : Optional[int]
    quantity : int
    order_status : Optional[str] = "PENDING"
    pizza_size : Optional[str] = "SMALL"
    flavour : str
    class Config:
        orm_mode = True
        schema_extra = {
            "example":{
                "quantity":2,
                "pizza_size":"LARGE",
                "order_status":"PENDING"
            }
        }


