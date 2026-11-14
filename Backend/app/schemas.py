from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    email: str
    password: str
    role: Optional[str] = "Customer"

class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    email: str
    role: str

    class Config:
        from_attributes = True    

from pydantic import BaseModel
from typing import List, Optional

# Menu Item Schema
class MenuItemCreate(BaseModel):
    name: str
    price: float
    restaurant_id: Optional[int] = 1
    is_available: int = 1

class MenuItemResponse(BaseModel):
    id: int
    name: str
    price: float
    is_available: int
    restaurant_id: int

    class Config:
        from_attributes = True

# Order Item Schema
class OrderItemBase(BaseModel):
    menu_item_id: int
    quantity: int

class OrderCreate(BaseModel):
    restaurant_id: int
    items: List[OrderItemBase]

class OrderResponse(BaseModel):
    id: int
    customer_id: int
    restaurant_id: int
    total_price: float
    status: str
    payment_status: str

class Config:
        from_attributes = True

class ReviewCreate(BaseModel):
    order_id: int
    rating: int
    comment: str    