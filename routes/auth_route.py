from fastapi import APIRouter,status,Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from database.database import get_db
from sqlalchemy.orm import Session
from schemas.auth_schema import RefreshRequest, SignUpModel,LoginModel
from database.models import User
from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder
from JWT.JWT_utils import create_access_token, create_refresh_token,verify_token
from utils.hashing_utils import hash_password,verify_password
from pydantic import BaseModel

from services.auth_service import AuthService

auth_router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

# Session is now managed per-request using Depends(get_db)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Gets the current authorized user
def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    return AuthService(db)


@auth_router.get('/',status_code=status.HTTP_201_CREATED)
def get_current_user(token: str = Depends(oauth2_scheme)):
    user_data = verify_token(token)
    if not user_data:
        raise HTTPException(status_code=401, detail="Invalid token")
    print(user_data)     
    return user_data  

@auth_router.post('/signup', response_model=SignUpModel, status_code=status.HTTP_201_CREATED)
async def signup(user_data: SignUpModel, db: Session = Depends(get_db),auth_service: AuthService = Depends(get_auth_service)):
    try:
            if auth_service.check_user_exist(user_data):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="User with this username or email already exists"
                )
            # Create new user
            hashed_password = hash_password(user_data.password)
            new_user = User(
                name=user_data.name,
                email=user_data.email,
                password=hashed_password,
                is_active=user_data.is_active,
                is_staff=user_data.is_staff
            )
            
            return auth_service.add_new_user(new_user)
            
    except HTTPException:
            raise
    except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create user"
            )


@auth_router.post("/login")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db),service: AuthService = Depends(get_auth_service)):
    user_db = service.authenticate_user(form_data)
    access_token = create_access_token(data={"sub": user_db.name, "userId": user_db.id})
    return {"access_token": access_token, "token_type": "bearer"}



@auth_router.post("/refresh")
def refresh_token(request: RefreshRequest):
    payload = verify_token(request.refresh_token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    
    new_access_token = create_access_token({"sub": payload["sub"]})
    return {"access_token": new_access_token}
