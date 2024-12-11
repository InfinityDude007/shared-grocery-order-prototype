from pydantic import BaseModel
from typing import List, Literal


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
    action: Literal['Update User Data', 'Add New User Data', 'Delete User Data']
    success: bool
    message: str
