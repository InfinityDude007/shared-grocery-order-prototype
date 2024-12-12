from .base_model import BaseModel
from sqlalchemy import String, Integer, Float, Column



class SupermarketProducts(BaseModel):
    __tablename__ = 'SupermarketProducts'

    product_id = Column(String(5), unique=True, nullable=False, primary_key=True)
    product_name = Column(String(50), unique=True, nullable=False)
    product_category = Column(String(50), nullable=False)
    product_price = Column(Float, nullable=False)
    product_stock = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<SupermarketProducts(ID = {self.product_id}, Name = {self.product_name}, Category = {self.product_category}, Price = {self.product_price}, Stock = {self.product_stock})>"