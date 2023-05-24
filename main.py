from fastapi import FastAPI
from ecommerce.user.routes import router as user_router
from ecommerce.products.routes import router as product_router
from ecommerce.cart.routes import router as cart_router
from ecommerce.orders.routes import router as order_router

app = FastAPI(
    title="Ecommerce API",
    version="0.0.1",
)

app.include_router(user_router)
app.include_router(product_router)
app.include_router(cart_router)
app.include_router(order_router)