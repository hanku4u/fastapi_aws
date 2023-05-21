from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ecommerce.db import get_db
from . import services, schema


router = APIRouter(
    prefix='/orders',
    tags=['orders']
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schema.ShowOrder)
async def initiate_order_processing(db: Session = Depends(get_db)):
    result = await services.initiate_order(db)
    return result


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[schema.ShowOrder])
async def orders_list(db: Session = Depends(get_db)):
    result = await services.get_order_listing(db)
    return result