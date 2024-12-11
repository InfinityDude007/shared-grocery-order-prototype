from .base_model import BaseModel
from sqlalchemy import String, Column, DateTime, Float
from datetime import datetime
    
class Orders(BaseModel):
    __tablename__ = 'Orders'
    
    order_id = Column(String(5), unique=True, nullable=False, primary_key=True)
    accommodation_id = Column(String(5), nullable=False)
    creation_date = Column(DateTime, default=datetime, nullable=False)
    order_status = Column(String(10), nullable= False)
    delivery_fee = Column(Float, nullable= False)
    
    def __repr__(self):
        return f"Orders(Order ID = {self.order_id}, Accommodation = {self.accommodation_id}, Date = {self.creation_date}, Status = {self.order_status}, Delivery = {self.delivery_fee})>"
