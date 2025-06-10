from fastapi import FastAPI
from routes import auth_route,order_route



app = FastAPI()

# setup jwt 1-create a class settings 2- generate secret key using secrets.token_hex()
# Create class login

app.include_router(auth_route.auth_router)
app.include_router(order_route.order_router)




