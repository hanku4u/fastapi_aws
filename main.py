from fastapi import FastAPI
import redis
from ecommerce.user.routes import router as user_router
from ecommerce.products.routes import router as product_router
from ecommerce.cart.routes import router as cart_router
from ecommerce.orders.routes import router as order_router

import debugpy
debugpy.listen(('0.0.0.0', 5678))

app = FastAPI(
    title="Ecommerce API",
    version="0.0.1",
)

r = redis.Redis(host='redis', port=6379, db=0)

app.include_router(user_router)
app.include_router(product_router)
app.include_router(cart_router)
app.include_router(order_router)

@app.get("/hits")
def read_root():
    r.incr('hits')
    return {"hits": r.get('hits')}  