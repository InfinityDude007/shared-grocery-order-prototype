from pydantic import BaseModel
from typing import List, Literal
from datetime import datetime


# schema for the details related to an individual order
class OrderData(BaseModel):
    order_id: str
    accommodation_id: str
    creation_date: datetime 
    order_status: str 
    delivery_fee: float 


# schema for the list of all order details available
class AllOrdersResponse(BaseModel):
    orders: List[OrderData]


# schema for showing the outcome of a put, post or delete request
class OrdersSuccessResponse(BaseModel):
    action: Literal['Update Order Data', 'Add New Order Data', 'Delete Order Data']
    success: bool
    message: str
