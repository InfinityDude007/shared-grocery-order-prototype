from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete
from server.dependencies import fetch_db_session
from server.schemas import UserData, AllUsersResponse, SuccessResponse
from server.models import Users

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
    query_result = await database.execute(select(Users))
    users = query_result.scalars().all()

    users_list = [
        UserData(
            user_id=user.user_id,
            first_name=user.first_name,
            last_name=user.last_name,
            email_id=user.email_id,
            phone_number=user.phone_number,
            accommodation_id=user.accommodation_id,
        )
        for user in users
    ]
    
    return AllUsersResponse(users=users_list)


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
    query_result = await database.get(Users, user_id)
    
    if not query_result:
        raise HTTPException(status_code=404, detail=f"User with ID '{user_id}' not found.")
    
    return UserData(
            user_id=query_result.user_id,
            first_name=query_result.first_name,
            last_name=query_result.last_name,
            email_id=query_result.email_id,
            phone_number=query_result.phone_number,
            accommodation_id=query_result.accommodation_id,
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
    id_query_result = await database.get(Users, request.user_id)
    email_query = await database.execute(select(Users).filter(Users.email_id == request.email_id))
    email_query_result = email_query.scalar_one_or_none()
    phone_query = await database.execute(select(Users).filter(Users.phone_number == request.phone_number))
    phone_query_result = phone_query.scalar_one_or_none()

    if id_query_result:
        raise HTTPException(status_code=409, detail=f"User with ID '{request.user_id}' already exists.")
    elif email_query_result:
        raise HTTPException(status_code=409, detail=f"User with email ID '{request.email_id}' already exists.")
    elif phone_query_result:
        raise HTTPException(status_code=409, detail=f"User with phone number '{request.phone_number}' already exists.")

    add_user = Users(
        user_id=request.user_id,
        first_name=request.first_name,
        last_name=request.last_name,
        email_id=request.email_id,
        phone_number=request.phone_number,
        accommodation_id=request.accommodation_id,
    )

    database.add(add_user)
    await database.commit()

    return SuccessResponse(
        action="Add New User Data",
        success=True,
        message=f"User with ID '{request.user_id}' and name '{request.first_name} {request.last_name}' added to database successfully!"
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
    query_result = await database.get(Users, user_id)

    if not query_result:
        raise HTTPException(status_code=404, detail=f"User with ID '{user_id}' not found.")
    
    email_query = await database.execute(select(Users).filter(Users.email_id == request.email_id))
    email_query_result = email_query.scalar_one_or_none()
    phone_query = await database.execute(select(Users).filter(Users.phone_number == request.phone_number))
    phone_query_result = phone_query.scalar_one_or_none()
    id_query_result = await database.get(Users, request.user_id)

    if email_query_result and email_query_result.user_id != user_id:
        raise HTTPException(status_code=409, detail=f"Email ID '{request.email_id}' already used with user ID '{email_query_result.user_id}'.")
    if phone_query_result and phone_query_result.user_id != user_id:
        raise HTTPException(status_code=409, detail=f"Phone number '{request.phone_number}' already used with user ID '{phone_query_result.user_id}'.")
    if id_query_result and id_query_result.user_id != user_id:
        raise HTTPException(status_code=409, detail=f"User ID '{request.user_id}' already exists for email ID '{id_query_result.email_id}'.")

    if query_result.user_id == request.user_id:
        success_response = SuccessResponse(
        action="Update Product Data",
        success=True,
        message=f"User data for ID '{user_id}' updated in database successfully!"
    )
    else:
        success_response = SuccessResponse(
        action="Update Product Data",
        success=True,
        message=f"User data for ID '{user_id}' updated in database successfully, new user ID is '{request.user_id}'."
    )

    query_result.user_id = request.user_id
    query_result.first_name = request.first_name
    query_result.last_name = request.last_name
    query_result.email_id = request.email_id
    query_result.phone_number = request.phone_number
    query_result.accommodation_id = request.accommodation_id

    await database.commit()

    return success_response


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
@router.delete("/delete/{user_id}", response_model=SuccessResponse)
async def delete_user(user_id: str, database: AsyncSession = Depends(fetch_db_session)) -> SuccessResponse:
    query_result = await database.get(Users, user_id)

    if not query_result:
        raise HTTPException(status_code=404, detail=f"User ID '{user_id}' not found.")

    await database.execute(delete(Users).filter(Users.user_id == user_id))
    await database.commit()

    return SuccessResponse(
        action="Delete User Data",
        success=True,
        message=f"User with ID '{user_id}' and email ID '{query_result.email_id}' deleted from database successfully!"
    )
