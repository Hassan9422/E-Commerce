from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import session
from app import schemas, database, models

router = APIRouter(
    prefix="/products", tags=["Products"]
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.ProductCreate)
def create_product(product: schemas.ProductCreate, db: session = Depends(database.get_db)):
    new_product = models.Product()

