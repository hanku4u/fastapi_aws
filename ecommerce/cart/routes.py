from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session

from ecommerce.db import get_db
from ecommerce.user.schema import User
from . import services
from . import schema


router = APIRouter(
    tags=['Cart'],
    prefix='/cart'
)


@router.get('/add', status_code=status.HTTP_201_CREATED)
async def add_product_to_cart(product_id: int, db: Session = Depends(get_db)):
    result = await services.add_to_cart(product_id, db)
    return result


@router.get('/', response_model=schema.ShowCart)
async def get_all_cart_items(db: Session = Depends(get_db)):
    result = await services.get_all_items(db)
    return result


@router.delete('/{cart_item_id}', status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def remove_cart_item_by_id(cart_item_id: int, db: Session = Depends(get_db)):
    await services.remove_cart_item(cart_item_id, db)
