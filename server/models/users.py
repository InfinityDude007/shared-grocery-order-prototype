from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from .base_model import BaseModel

class User(BaseModel):
    __tablename__ = "Users"

    user_id = Column(String(5), primary_key=True, unique=True, nullable=False)
    first_name = Column(String(30), nullable=False)
    last_name = Column(String(30), nullable=False)
    email_id = Column(String(150), unique=True, nullable=False)
    phone_number = Column(String(15), unique=True, nullable=False)
    accommodation_id = Column(String(5), nullable=True)
    

    def __repr__(self):
         return f"<User(User ID={self.user_id}, Name={self.first_name} {self.last_name}, Email ID={self.email_id}, accommodation_id={self.accommodation_id})>"
