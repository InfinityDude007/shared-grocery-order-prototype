from .base_model import BaseModel
from sqlalchemy import String, Integer, Float, Table, Column
from sqlalchemy.orm import relationship



class Supermarket(BaseModel):
    __tablename__ = 'SupermarketProducts'

    product_id = Column(String(5), unique=True, nullable=False, primary_key=True)
    product_name = Column(String(50), unique=True, nullable=False)
    product_price = Column(Float, nullable=False)
    product_stock = Column(Integer, nullable=False)

    def __repr__(self):
        return f"Supermarket(name'{self.product_name}')>"