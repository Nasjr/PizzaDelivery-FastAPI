from typing import Optional
from pydantic import BaseModel

class SignUpModel(BaseModel):
    id : Optional[int]
    name : str
    email : str
    password: str
    is_active: Optional[bool]
    is_staff: Optional[bool]

    class Config:
        orm_mode= True
        schema_extra={
            'example':{
                "userName":"johnde",
                "Email":"johnde@gmail.com",
                "password":"P@ssword",
                "is_staff:": True,
                "is_active:":False,
            }
        }


class RefreshRequest(BaseModel):
    refresh_token: str
class LoginModel(BaseModel):
    username:str
    password:str