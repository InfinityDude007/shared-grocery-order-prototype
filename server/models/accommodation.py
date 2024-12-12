from .base_model import BaseModel
from sqlalchemy import String, Column
from typing import List
    
class Accommodation(BaseModel):
    __tablename__ = 'Accommodation'
    
    accommodation_id = Column(String(5), unique=True, nullable=False, primary_key=True)
    accommodation_users = Column(List[String], nullable=False)
    
    def __repr__(self):
        return f"<Accommodation(Accommodation ID = {self.accommodation_id}, Users = {self.accommodation_users})>"