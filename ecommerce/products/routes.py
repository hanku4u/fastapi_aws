from typing import List
from fastapi import APIRouter, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session

from ecommerce.db import get_db
from . import schema
from . import services
from . import validator


router = APIRouter(
    tags=['Products'],
    prefix='/products'
)


@router.post('/category', status_code=status.HTTP_201_CREATED)
async def create_category(request: schema.Category, db: Session = Depends(get_db)):
    new_category = await services.create_new_category(request, db)
    return new_category


@router.get('/category', response_model=List[schema.ListCategory])
async def get_all_categories(db: Session = Depends(get_db)):
    return await services.all_categories(db)


@router.get('/category/{category_id}', status_code=status.HTTP_200_OK, response_model=schema.ListCategory)
async def get_category_by_id(category_id: int, db: Session = Depends(get_db)):
    return await services.get_category_by_id(category_id, db)


@router.delete('/category/{category_id}', status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def delete_category_by_id(category_id: int, db: Session = Depends(get_db)):
    return await services.delete_category_by_id(category_id, db)


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_product(request: schema.Product, db: Session = Depends(get_db)):
    category = await validator.verify_category_exist(request.category_id, db)
    if not category:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Category not found')
    
    product = await services.create_new_product(request, db)
    return product


@router.get('/', response_model=List[schema.ProductListing])
async def get_all_products(db: Session = Depends(get_db)):
    return await services.get_all_products(db)