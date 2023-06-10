from typing import List, Optional
from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy import func
from sqlalchemy.orm import session
from app import schemas, database, models, OAuth2

router = APIRouter(
    prefix="/products", tags=["Products"]
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ProductResponse)
def create_product(product: schemas.ProductCreate, db: session = Depends(database.get_db), current_user=Depends(
    OAuth2.verify_and_get_current_user)):
    new_product = models.Product(product_owner_id=current_user.id, **product.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product


@router.get("/", response_model=List[schemas.ProductResponse])
def get_all_products(db: session = Depends(database.get_db), search: Optional[str] = "", current_user=Depends(
    OAuth2.verify_and_get_current_user), limit: int = 10, skip: int = 0):
    all_products = db.query(models.Product, func.count(models.Vote.user_id).label("vote_number")).join(models.Vote, models.Product.id ==
                                                                                        models.Vote.product_id, isouter=True).group_by(
        models.Product.id).filter(
        models.Product.name.contains(
        search)).limit(limit).offset(
        skip).all()

    if not all_products:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Sorry! there are no products in the store recently!")

    print(type(all_products))
    return all_products


@router.get("/{id}", response_model=schemas.ProductResponse)
def get_one_product(id: int, db: session = Depends(database.get_db), current_user=Depends(OAuth2.verify_and_get_current_user)):
    one_product_query = db.query(models.Product, func.count(models.Vote.user_id).label("vote_number")).join(models.Vote, models.Product.id ==
                                                                                        models.Vote.product_id, isouter=True).group_by(
        models.Product.id).filter(
        models.Product.id == id)
    # .join(models.User, models.Product.product_owner_id == models.User.id)
    if not one_product_query.first():
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f'product with id={id} does not exist!')

    return one_product_query.first()


@router.put("/{id}", response_model=schemas.ProductResponse)
def update_one_product(id: int, product: schemas.ProductCreate, db: session = Depends(database.get_db), current_user=Depends(
    OAuth2.verify_and_get_current_user)):
    found_product_query = db.query(models.Product).filter(models.Product.id == id)

    if not found_product_query.first():
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"Product with id={id} does not exist!")

    if current_user.id != found_product_query.first().product_owner_id and current_user.role != 'admin':
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail=f"You are not allowed to perform this action!")

    found_product_query.update(product.dict(), synchronize_session=False)
    db.commit()

    return found_product_query.first()


@router.delete("/{id}")
def delete_one_product(id: int, db: session = Depends(database.get_db), current_user=Depends(OAuth2.verify_and_get_current_user)):
    found_product_query = db.query(models.Product).filter(models.Product.id == id)

    if not found_product_query.first():
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"Product with id={id} does not exist!")

    if current_user.id != found_product_query.first().product_owner_id and current_user.role != 'admin':
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail=f"You are not allowed to perform this action!")

    found_product_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

