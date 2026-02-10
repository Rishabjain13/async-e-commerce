from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.product_routes import router as user_router
from app.routes.product_transaction_routes import router as admin_router
from app.routes.cart_routes import router as cart_router
from app.routes.order_routes import router as order_router
from app.routes.address_routes import router as address_router
from app.routes.shipping_routes import router as shipping_router
from app.routes.search_routes import router as search_router
from app.routes.payment_routes import router as payment_router
from app.routes.health import router as health_router
from app.routes.auth_routes import router as auth_router
from app.routes.admin_routes import router as admin_router

app = FastAPI(title="Async E-commerce API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(admin_router)
app.include_router(cart_router)
app.include_router(order_router)
app.include_router(address_router)
app.include_router(shipping_router)
app.include_router(search_router)
app.include_router(payment_router)
app.include_router(health_router)
app.include_router(auth_router)
