from pydantic import BaseModel
from typing import List, Literal


# schema for the details related to an individual user
class UserData(BaseModel):
    user_id: str
    first_name: str
    last_name: str
    email_id: str
    phone_number: str
    accommodation_id: str


# schema for the list of all user details available
class AllUsersResponse(BaseModel):
    users: List[UserData]


# schema for showing the outcome of a put, post or delete request
class UsersSuccessResponse(BaseModel):
    action: Literal['Update User Data', 'Add New User Data', 'Delete User Data']
    success: bool
    message: str
