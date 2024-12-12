from .base_model import BaseModel
from sqlalchemy import String, Column, DateTime, Float
from datetime import datetime
    
class Orders(BaseModel):
    __tablename__ = 'Orders'
    
    order_id = Column(String(5), unique=True, nullable=False, primary_key=True)
    accommodation_id = Column(String(5), nullable=False)
    creation_date = Column(DateTime, default=datetime, nullable=False)
    order_status = Column(String(10), nullable= False)
    items_cost = Column(Float, nullable=False)
    delivery_fee = Column(Float, nullable=False)
    order_total = Column(Float, nullable=False)
    
    def __repr__(self):
        return f"<Orders(ID = {self.order_id}, Accommodation ID = {self.accommodation_id}, Date = {self.creation_date}, Status = {self.order_status}, Items total = {self.items_cost}, Delivery = {self.delivery_fee}, Order total = {self.order_total})>"
