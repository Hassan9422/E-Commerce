from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import session
from app import schemas, database, models

router = APIRouter(
    prefix="/users", tags=["Users"]
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.UserRegister, db: session = Depends(database.get_db)):
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/{id}", response_model=schemas.UserResponse)
def get_one_user(db: session = Depends(database.get_db), id: int = id):
    one_post = db.query(models.User).filter(models.User.id == id).first()
    if not one_post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"user with id={id} does not exist.")

    return one_post
