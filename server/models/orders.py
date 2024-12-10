from .base_model import BaseModel
from sqlalchemy import String, Column, DateTime, Enum, Float
from datetime import datetime
import enum

class OrderStatusEnum(enum.Enum):
    pending = "Pending"
    compleated = "Compleated"
    canclled = "Cancelled"
    
    
class Orders(BaseModel):
    __tablename__ = 'Orders'
    
    order_id = Column(String(5), unique=True, nullable=False, primary_key=True)
    accmodation_id = Column(String(5), unique=True, nullable=False)
    creation_date = Column(DateTime, default=datetime.timezone.utc, nullable=False)
    order_status = Column(Enum(OrderStatusEnum), nullable= False)
    delivery_fee = Column(Float, nullable= False)
    
    def __repr__(self):
        return f"Orders(Order ID = {self.order_id}, Accmodation = {self.accmodation_id_id}, Date = {self.creation_date}, Status = {self.order_status}, Delivery = {self.delivery_fee})>"
