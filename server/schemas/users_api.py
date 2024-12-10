from pydantic import BaseModel
from typing import List


class UserData(BaseModel):
    user_id: str
    first_name: str
    last_name: str
    email_id: str
    phone_number: str
    accommodation_id: str


class AllUsersResponse(BaseModel):
    users: List[UserData]


class SuccessResponse(BaseModel):
    action: str
    success: bool
    message: str
