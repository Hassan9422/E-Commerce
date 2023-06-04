from fastapi import FastAPI

from app import models
from app.database import engine
from app.routers import users, products

app = FastAPI()
models.Base.metadata.create_all(bind=engine)


app.include_router(users.router)
app.include_router(products.router)
