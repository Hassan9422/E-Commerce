from datetime import datetime
from typing import Optional

from pydantic import EmailStr, BaseModel, validator


class UserBase(BaseModel):
    name: str
    email: EmailStr


class ProductBase(BaseModel):
    name: str
    category: str
    original_price: float
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
    role: str
    password: str
    phone_number: int
    city: str

    @validator('role')
    def role_match(cls, value):
        if value not in ['user', 'admin']:
            raise ValueError("enter a correct role name. choose from ['user', 'admin']")
        return value


class UserResponse0(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    User: UserResponse0
    product_number: int

    class Config:
        orm_mode = True


class ProductCreate(ProductBase):
    pass


class ProductResponse0(ProductBase):
    id: int
    product_owner_id: int
    new_price: float
    created_at: datetime
    owner: UserResponse0

    class Config:
        orm_mode = True


class ProductResponse(BaseModel):
    Product: ProductResponse0
    vote_number: int

    class Config:
        orm_mode = True


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    token: str
    token_type: str


class TokenData(BaseModel):
    id: int
    name: str
    role: str

    class Config:
        orm_mode = True


class Vote(BaseModel):
    product_id: int
    dir: bool
