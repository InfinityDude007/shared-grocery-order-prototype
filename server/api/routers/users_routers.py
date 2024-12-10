from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from server.dependencies import fetch_db_session
from server.schemas import UserData, AllUsersResponse, SuccessResponse

router = APIRouter()


@router.get("/all", response_model=AllUsersResponse)
async def fetch_all_users(database: AsyncSession = Depends(fetch_db_session)) -> AllUsersResponse:
    """
    Function Overview:
    Fetches all users from the database.

    Function Logic:
    1. Use the database session to query the users table.
    2. Return fetched users as a list of UserData schemas.
    3. Wrap the list in an AllUsersResponse schema.

    Parameters:
    database (AsyncSession): Database session dependency to interact with the database.

    Returns:
    AllUsersResponse: A response containing a list of all users.
    """
    # function logic to be added here

    # return mock data for testing route
    return AllUsersResponse(
        users=[
            UserData(
                user_id="1001",
                first_name="John",
                last_name="Doe",
                email_id="john.doe@example.com",
                phone_number="+971501234567",
                accommodation_id="1001"
            ),
            UserData(
                user_id="1002",
                first_name="Jane",
                last_name="Smith",
                email_id="jane.smith@example.com",
                phone_number="+971502345678",
                accommodation_id="1002"
            )
        ]
    )


@router.get("/{user_id}", response_model=UserData)
async def fetch_user(user_id: str, database: AsyncSession = Depends(fetch_db_session)) -> UserData:
    """
    Function Overview:
    Fetches details of a specific user based on the provided user ID.

    Function Logic:
    1. Use the user_id parameter to query the database for user data.
    2. Return user data wrapped in a UserData schema.

    Parameters:
    user_id (str): ID of the user to fetch.
    database (AsyncSession): Database session dependency to interact with the database.

    Returns:
    UserData: Details of the requested user.
    """
    # function logic to be added here

    # return mock data for testing route
    return UserData(
        user_id="1001",
        first_name="John",
        last_name="Doe",
        email_id="john.doe@example.com",
        phone_number="+971501234567",
        accommodation_id="1001"
    )


@router.post("/add", response_model=SuccessResponse)
async def add_user(request: UserData, database: AsyncSession = Depends(fetch_db_session)) -> SuccessResponse:
    """
    Function Overview:
    Adds a new user to the database.

    Function Logic:
    1. Use incoming request data in UserData schema to create a new user record.
    2. Insert new user data into the database.
    3. Return a success message wrapped in a SuccessResponse schema.

    Parameters:
    request (UserData): User data to be added.
    database (AsyncSession): Database session dependency to interact with the database.

    Returns:
    SuccessResponse: A response indicating whether the user was added successfully.
    """
    # function logic to be added here

    # return mock data for testing route
    return SuccessResponse(
        action="Add New User",
        success=True,
        message=f"User with ID {request.user_id} added successfully!"
    )


@router.put("/update/{user_id}", response_model=SuccessResponse)
async def update_user(user_id: str, request: UserData, database: AsyncSession = Depends(fetch_db_session)) -> SuccessResponse:
    """
    Function Overview:
    Updates details of a specific user in the database.

    Function Logic:
    1. Use the user_id to locate the existing user in the database.
    2. Apply updates based on incoming request data in UserData schema.
    3. Return a success message wrapped in a SuccessResponse schema.

    Parameters:
    user_id (str): ID of the user to update.
    request (UserData): Updated user data.
    database (AsyncSession): Database session dependency to interact with the database.

    Returns:
    SuccessResponse: A response indicating whether the update was successful.
    """
    # function logic to be added here

    # return mock data for testing route
    return SuccessResponse(
        action="Update User",
        success=True,
        message=f"User with ID {user_id} updated successfully!"
    )


@router.delete("/delete/{user_id}", response_model=SuccessResponse)
async def delete_user(user_id: str, database: AsyncSession = Depends(fetch_db_session)) -> SuccessResponse:
    """
    Function Overview:
    Deletes a specific user from the database based on the provided user ID.

    Function Logic:
    1. Use the user_id to locate the user in the database.
    2. Remove the user from the database.
    3. Return a success message wrapped in a SuccessResponse schema.

    Parameters:
    user_id (str): ID of the user to delete.
    database (AsyncSession): Database session dependency to interact with the database.

    Returns:
    SuccessResponse: A response indicating whether the deletion was successful.
    """
    # function logic to be added here

    # return mock data for testing route
    return SuccessResponse(
        action="Delete User",
        success=True,
        message=f"User with ID {user_id} deleted successfully!"
    )
