from pydantic import BaseModel
from typing import List, Optional, Literal
from decimal import Decimal
from app.core.orders_workflow import OrderStatus
from datetime import datetime

class OrderItemCreate(BaseModel):
    variant_id: int
    sku: str
    name: str
    qty: int
    unit_price: Decimal
    
class OrderCreate(BaseModel):
    customer_name: str
    customer_phone: str
    delivery_type: Literal["delivery", "pickup"]
    delivery_address: Optional[str] = None
    notes: Optional[str] = None
    items: List[OrderItemCreate]

class OrderItemResponse(BaseModel):
    id: int
    variant_id: int
    sku: str
    name: str
    qty: int
    unit_price: Decimal

    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    id: int
    status: str
    customer_name: str
    customer_phone: str
    delivery_type: str
    delivery_address: Optional[str] = None
    notes: Optional[str] = None
    items: List[OrderItemResponse]

    class Config:
        from_attributes = True

class OrderStatusUpdate(BaseModel):
    status: OrderStatus

class OrderListItem(BaseModel):
    id: int
    status: OrderStatus
    customer_name: str
    customer_phone: str
    delivery_type: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class OrderListResponse(BaseModel):
    items: List[OrderListItem]
    total: int
    limit: int
    offset: int