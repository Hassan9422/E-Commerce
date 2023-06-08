from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import session
from app import schemas, database, models, hash, OAuth2

router = APIRouter(
    prefix="/users", tags=["Users"]
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.UserRegister, db: session = Depends(database.get_db)):
    user.password = hash.password_hash(user.password)
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/{id}", response_model=schemas.UserResponse)
def get_one_user(db: session = Depends(database.get_db), id: int = id, current_user=Depends(OAuth2.verify_and_get_current_user)):
    # one_user = db.query(models.User).filter(models.User.id == id).first()
    one_user = db.query(models.User, func.count(models.Product.id).label("product_number")).join(models.Product,
                                                                                                            models.User.id
                                                                                                            == models.Product.product_owner_id).group_by(
        models.User.id).filter(models.User.id == id)
    print(one_user)

    if not one_user.first():
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"user with id={id} does not exist.")

    return one_user.first()
