from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class OrderBase(BaseModel):
    product_type: str
    product_name: str
    amount: float

class OrderCreate(OrderBase):
    order_state: str

class OrderUpdate(BaseModel):
    order_state: str

class OrderResponse(OrderBase):
    id: UUID
    order_state: str
    created_at: datetime
    last_modified: Optional[datetime]

    class Config:
        orm_mode = True
