import json
from datetime import timedelta, datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import session
from app import database, schemas, models
from app.config import setting
from jose import jwt, JWTError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = setting.secret_key
ALGORITHM = setting.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = setting.access_token_expire_minutes


def create_access_token(data: dict):
    payload_data = data.copy()
    expiration_time_field = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload_data.update({"expire": f"{expiration_time_field}"})
    encoded_jwt = jwt.encode(payload_data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_and_get_current_user(token: str = Depends(oauth2_scheme), db: session = Depends(database.get_db)):
    credentials_exception = HTTPException(status.HTTP_403_FORBIDDEN, detail="You are not authorized!")

    try:
        payload_data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id, name, role = payload_data.get("id"), payload_data.get("name"), payload_data.get("role")

        if not id or not name or not role:
            raise credentials_exception

        # basically, "token_payload" in line below is a pydantic object which we have created from the "TokenData" pydantic class. now that we
        # have this object, we can access its properties which are "name", "id" and "role".
        token_payload = schemas.TokenData(**{"id": id, "name": name, "role": role})

    except JWTError:
        raise credentials_exception

    # now we can perform a query to our database to retrieve the user after seeing no errors:
    corresponding_user = db.query(models.User).filter(models.User.id == token_payload.id, models.User.name == token_payload.name,
                                                      models.User.role == token_payload.role).first()

    if not corresponding_user:
        raise credentials_exception

    return corresponding_user
