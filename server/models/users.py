from sqlalchemy import Column, String
from .base_model import BaseModel



class Users(BaseModel):
    __tablename__ = "Users"

    user_id = Column(String(5), primary_key=True, unique=True, nullable=False)
    first_name = Column(String(30), nullable=False)
    last_name = Column(String(30), nullable=False)
    email_id = Column(String(100), unique=True, nullable=False)
    phone_number = Column(String(15), unique=True, nullable=False)
    accommodation_id = Column(String(5), nullable=True)

    def __repr__(self):
         return f"<User(ID = {self.user_id}, Name = {self.first_name} {self.last_name}, Email ID = {self.email_id}, Accommodation ID = {self.accommodation_id})>"
