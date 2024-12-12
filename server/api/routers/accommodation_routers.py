from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete
from server.dependencies import fetch_db_session
from server.schemas import AllAccommodationsResponse, AccommodationSuccessResponse, AccommodationData
from server.models import Accommodation

router = APIRouter()



@router.get("/all", response_model=AllAccommodationsResponse)
async def fetch_all_accommodations(database: AsyncSession = Depends(fetch_db_session)) -> AllAccommodationsResponse:
    """
    Function Overview:
    Fetches all accommodations from the database.

    Function Logic:
    1. Query the database for all accommodation records.
    2. Transform the database results into a list of AccommodationData schemas.
    3. Return the list wrapped in an AllAccommodationsResponse schema.

    Parameters:
    database (AsyncSession): Database session dependency to interact with the database.

    Returns:
    AllAccommodationsResponse: A response containing a list of all accommodations.
    """
    query_result = await database.execute(select(Accommodation))
    accommodations = query_result.scalars().all()

    accommodations_list = [
        AccommodationData(
            accommodation_id=accommodation.accommodation_id,
            accommodation_users=accommodation.accommodation_users
        )
        for accommodation in accommodations
    ]

    return AllAccommodationsResponse(accommodations=accommodations_list)


@router.get("/{accommodation_id}", response_model=AccommodationData)
async def fetch_accommodation(accommodation_id: str, database: AsyncSession = Depends(fetch_db_session)) -> AccommodationData:
    """
    Function Overview:
    Fetches details of a specific accommodation based on the provided accommodation ID.

    Function Logic:
    1. Query the database for the accommodation record with the given ID.
    2. If the record exists, return it wrapped in an AccommodationData schema.
    3. If the record does not exist, raise a 404 error.

    Parameters:
    accommodation_id (str): ID of the accommodation to fetch.
    database (AsyncSession): Database session dependency to interact with the database.

    Returns:
    AccommodationData: Details of the requested accommodation.
    """
    query_result = await database.get(Accommodation, accommodation_id)

    if not query_result:
        raise HTTPException(status_code=404, detail=f"Accommodation with ID '{accommodation_id}' not found.")

    return AccommodationData(
        accommodation_id=query_result.accommodation_id,
        accommodation_users=query_result.accommodation_users
    )


@router.post("/add", response_model=AccommodationSuccessResponse)
async def add_accommodation(request: AccommodationData, database: AsyncSession = Depends(fetch_db_session)) -> AccommodationSuccessResponse:
    """
    Function Overview:
    Adds a new accommodation to the database.

    Function Logic:
    1. Check if an accommodation with the given ID already exists in the database.
    2. If it exists, raise a 409 error to indicate a conflict.
    3. If it does not exist, create a new Accommodation record and add it to the database.
    4. Commit the changes and return a success response.

    Parameters:
    request (AccommodationData): Data for the new accommodation.
    database (AsyncSession): Database session dependency to interact with the database.

    Returns:
    AccommodationSuccessResponse: A response indicating whether the accommodation was added successfully.
    """
    existing_accommodation = await database.get(Accommodation, request.accommodation_id)

    if existing_accommodation:
        raise HTTPException(status_code=409, detail=f"Accommodation with ID '{request.accommodation_id}' already exists.")

    new_accommodation = Accommodation(
        accommodation_id=request.accommodation_id,
        accommodation_users=request.accommodation_users
    )

    database.add(new_accommodation)
    await database.commit()

    return AccommodationSuccessResponse(
        action="Add New Accommodation",
        success=True,
        message=f"Accommodation with ID '{request.accommodation_id}' added successfully!"
    )


@router.put("/update/{accommodation_id}", response_model=AccommodationSuccessResponse)
async def update_accommodation(accommodation_id: str, request: AccommodationData, database: AsyncSession = Depends(fetch_db_session)) -> AccommodationSuccessResponse:
    """
    Function Overview:
    Updates details of a specific accommodation in the database.

    Function Logic:
    1. Query the database for the accommodation record with the given ID.
    2. If the record does not exist, raise a 404 error.
    3. If the record exists, update its fields with the new data from the request.
    4. Commit the changes and return a success response.

    Parameters:
    accommodation_id (str): ID of the accommodation to update.
    request (AccommodationData): Updated data for the accommodation.
    database (AsyncSession): Database session dependency to interact with the database.

    Returns:
    AccommodationSuccessResponse: A response indicating whether the update was successful.
    """
    query_result = await database.get(Accommodation, accommodation_id)

    if not query_result:
        raise HTTPException(status_code=404, detail=f"Accommodation with ID '{accommodation_id}' not found.")

    query_result.accommodation_users = request.accommodation_users

    await database.commit()

    return AccommodationSuccessResponse(
        action="Update Accommodation Data",
        success=True,
        message=f"Accommodation with ID '{accommodation_id}' updated successfully!"
    )


@router.delete("/delete/{accommodation_id}", response_model=AccommodationSuccessResponse)
async def delete_accommodation(accommodation_id: str, database: AsyncSession = Depends(fetch_db_session)) -> AccommodationSuccessResponse:
    """
    Function Overview:
    Deletes a specific accommodation from the database based on the provided accommodation ID.

    Function Logic:
    1. Query the database for the accommodation record with the given ID.
    2. If the record does not exist, raise a 404 error.
    3. If the record exists, delete it from the database.
    4. Commit the changes and return a success response.

    Parameters:
    accommodation_id (str): ID of the accommodation to delete.
    database (AsyncSession): Database session dependency to interact with the database.

    Returns:
    AccommodationSuccessResponse: A response indicating whether the deletion was successful.
    """
    query_result = await database.get(Accommodation, accommodation_id)

    if not query_result:
        raise HTTPException(status_code=404, detail=f"Accommodation ID '{accommodation_id}' not found.")

    await database.execute(delete(Accommodation).filter(Accommodation.accommodation_id == accommodation_id))
    await database.commit()

    return AccommodationSuccessResponse(
        action="Delete Accommodation Data",
        success=True,
        message=f"Accommodation with ID '{accommodation_id}' deleted successfully!"
    )
