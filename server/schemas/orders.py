from pydantic import BaseModel, Field
from typing import List, Literal
from datetime import datetime

class OrderData(BaseModel):
    order_id: str
    accommodation_id: str
    creation_date: datetime 
    order_status: str 
    delivery_fee: float 

class AllOrdersResponse(BaseModel):
    orders: List[OrderData]

class SuccessResponse(BaseModel):
    action: Literal['Update Order Data', 'Add New Order', 'Delete Order']
    success: bool
    message: str
