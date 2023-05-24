from typing import List
from fastapi import HTTPException, status

from ecommerce.orders.order_models import Order, OrderDetails
from ecommerce.cart.cart_models import Cart, CartItems
from ecommerce.user.user_models import User


async def initiate_order(db) -> Order:
    user_info = db.query(User).filter(User.email == 'test@example.com').first()
    cart = db.query(Cart).filter(Cart.user_id == user_info.id).first()

    cart_items_objects = db.query(CartItems).filter(Cart.id == cart.id)
    if not cart_items_objects:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Cart is empty')
    
    total_amount = 0.0
    for item in cart_items_objects:
        total_amount += item.product.price

    new_order = Order(order_amount=total_amount,
                    customer_id=user_info.id,
                    shipping_address="587 go fuck yourself ave, bumfuck, Iowa")
    
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    bulk_order_details_objects = list()

    for item in cart_items_objects:
        new_order_details = OrderDetails(order_id=new_order.id,
                                        product_id=item.product.id)
        bulk_order_details_objects.append(new_order_details)

        db.bulk_save_objects(bulk_order_details_objects)
        db.commit()

        # send email
        # TODO will work later

        # clear items in the cart
        db.query(CartItems).filter(CartItems.cart_id == cart.id).delete()
        db.commit()

        return new_order
    

async def get_order_listing(db) -> List[Order]:
    user_info = db.query(User).filter(User.email == "test@example.com").first()
    orders = db.query(Order).filter(Order.customer_id == user_info.id).all()

    return orders