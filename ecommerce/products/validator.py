from typing import Optional
from sqlalchemy.orm import Session
from . product_models import Category


async def verify_category_exist(category_id: int, db: Session) -> Optional[Category]:
    return db.query(Category).filter(Category.id == category_id).first()