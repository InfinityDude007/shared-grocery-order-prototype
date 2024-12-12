from .base_model import BaseModel
from sqlalchemy import String, Column, JSON, Float, Boolean
from datetime import datetime

class CostSplitting(BaseModel):
    __tablename__ = "CostSplitting"

    user_id =  Column(String(5), unique=True, nullable=False, primary_key=True)
    accomodation_id = Column(String(5), nullable=False)
    order_id =  Column(String(5), unique=True, nullable=False)
    order_items = Column(JSON, nullable=False)
    share_cost = Column(Float, nullable=False)
    payment = Column(Boolean, nullable=False)
    delivery_fee_split = Column(Float, nullable=False)
    total_split = Column(Float, nullable=False)

    def __repr__(self):
        return f"<CostSplitting(User ID = {self.user_id}, Accommodation ID = {self.accomodation_id}, Order ID = {self.order_id}, Items = {self.order_items}, Share Cost = {self.share_cost}, Payment = {self.payment}, Delivery Fee = {self.delivery_fee_split}, Total Split = {self.total_split})>"
