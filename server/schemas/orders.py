from pydantic import BaseModel, Field
from typing import List, Literal
from datetime import datetime

class SharedOrderData(BaseModel):
    order_id: str
    group_id: str
    creation_date: datetime 
    order_status: str 
    delivery_fee: float 

class AllSharedOrdersResponse(BaseModel):
    orders: List[SharedOrderData]

class SuccessResponse(BaseModel):
    action: Literal['Update Order Data', 'Add New Order', 'Delete Order']
    success: bool
    message: str
