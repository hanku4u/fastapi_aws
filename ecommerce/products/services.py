from fastapi import HTTPException, status
from . import product_models


async def create_new_category(request, db) -> product_models.Category:
    new_category = product_models.Category(name=request.name)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


async def all_categories(db) -> list[product_models.Category]:
    categories = db.query(product_models.Category).all()
    return categories


async def get_category_by_id(category_id: int, db) -> product_models.Category:
    category = db.query(product_models.Category).get(category_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Category with id {category_id} not found')
    return category


async def delete_category_by_id(category_id: int, db) -> None:
    category = db.query(product_models.Category).get(category_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Category with id {category_id} not found')
    db.delete(category)
    db.commit()
    return None


async def create_new_product(request, db) -> product_models.Product:
    new_product = product_models.Product(name=request.name, description=request.description, price=request.price,
                                        category_id=request.category_id)
    
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


async def get_all_products(db) -> list[product_models.Product]:
    products = db.query(product_models.Product).all()
    return products