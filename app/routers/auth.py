from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import session
from app import schemas, database, models, hash, OAuth2

router = APIRouter(
    prefix="/login"
)


@router.post("/", response_model=schemas.LoginResponse)
def login(user: schemas.LoginRequest, db: session = Depends(database.get_db)):
    found_user = db.query(models.User).filter(models.User.email == user.email).first()

    if not found_user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"wrong credentials!")

    check_password = hash.verify_password(user.password, found_user.password)

    if not check_password:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="wrong credentials!")

    # data dictionary in line below is a set of information which we wanna encode in the jwt token as payload data:
    access_token = OAuth2.create_access_token(data={"id": found_user.id, "name": found_user.name, "role": found_user.role})
    return {"token": access_token, "token_type": "Bearer"}

