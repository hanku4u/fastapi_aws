from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session

from ecommerce.db import get_db
from ecommerce.products.product_models import Product
from ecommerce.user.user_models import User
from . cart_models import Cart, CartItems
import ecommerce.cart.schema as schema


async def add_items(cart_id, product_id, database: Session = Depends(get_db)):
    cart_items = CartItems(cart_id=cart_id, product_id=product_id)
    database.add(cart_items)
    database.commit()
    database.refresh(cart_items)


async def add_to_cart(product_id, db: Session = Depends(get_db)):
    product = db.query(Product).get(product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Date not found")
    
    if product.quantity <= 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product out of stock")
    
    user_info = db.query(User).filter(User.email == 'test@example.com').first()

    cart_info = db.query(Cart).filter(Cart.user_id == user_info.id).first()
    
    if not cart_info:
        new_cart = Cart(user_id=user_info.id)
        db.add(new_cart)
        db.commit()
        db.refresh(new_cart)
        await add_items(new_cart.id, product_id, db)
    else:
        await add_items(cart_info.id, product_id, db)

    return {"status": "Item Added to cart"}


async def get_all_items(db: Session = Depends(get_db)) -> schema.ShowCart:
    user_info = db.query(User).filter(User.email == 'test@example.com').first()
    cart = db.query(Cart).filter(Cart.user_id == user_info.id).first()
    return cart


async def remove_cart_item(cart_item_id: int, db) -> None:
    user_info = db.query(User).filter(User.email == 'test@example.com').first()
    cart_id = db.query(Cart).filter(Cart.user_id == user_info.id).first()

    db.query(CartItems).filter(CartItems.id == cart_item_id,
                            CartItems.cart_id == cart_id.id).delete()
    
    db.commit()
    return