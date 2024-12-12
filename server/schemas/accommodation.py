from pydantic import BaseModel
from typing import List, Literal


# Schema for the details related to an individual accommodation
class AccommodationData(BaseModel):
    accommodation_id: str
    accommodation_users: List[str]


# Schema for the list of all accommodation details available
class AllAccommodationsResponse(BaseModel):
    accommodations: List[AccommodationData]


# Schema for showing the outcome of a put, post, or delete request
class AccommodationSuccessResponse(BaseModel):
    action: Literal['Update Accommodation Data', 'Add New Accommodation Data', 'Delete Accommodation Data']
    success: bool
    message: str
