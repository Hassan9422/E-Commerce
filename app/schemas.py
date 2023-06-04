from datetime import datetime
from typing import Optional

from pydantic import EmailStr, BaseModel, validator


class UserBase(BaseModel):
    name: str
    email: EmailStr


class ProductBase(BaseModel):
    name: str
    category: str
    original_price: int
    discount: float

    @validator('category')
    def category_match(cls, value):
        if value not in ['food', 'cleaning', 'drink', 'electronic device']:
            raise ValueError("enter a correct category name. choose from ['food', 'cleaning', 'drink', 'electronic device']")
        return value

    @validator('discount')
    def discount_check(cls, d):
        if d < 0 or d > 1:
            raise ValueError("discount should not be greater than 1 or negative.")
        return d


class UserRegister(UserBase):
    password: str
    phone_number: int
    city: str


class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class ProductCreate(ProductBase):
    pass


class ProductResponse(ProductBase):
    id: int
    created_at: datetime

