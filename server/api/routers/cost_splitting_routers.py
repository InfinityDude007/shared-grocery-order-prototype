from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete
from server.dependencies import fetch_db_session
from server.schemas import CostSplittingData, AllCostSplittingsResponse, CostSplittingsSuccessResponse
from server.models import CostSplitting

router = APIRouter()


@router.get("/all", response_model=AllCostSplittingsResponse)
async def fetch_all_cost_splittings(database: AsyncSession = Depends(fetch_db_session)) -> AllCostSplittingsResponse:
    """
    Function Overview:
    Fetches all cost splitting entries from the database.

    Function Logic:
    1. Use the database session to query the CostSplitting table.
    2. Return fetched entries as a list of CostSplittingData schemas.
    3. Wrap the list in an AllCostSplittingsResponse schema.

    Parameters:
    database (AsyncSession): Database session dependency to interact with the database.

    Returns:
    AllCostSplittingsResponse: A response containing a list of all cost splitting entries.
    """
    query_result = await database.execute(select(CostSplitting))
    cost_splittings = query_result.scalars().all()

    cost_splittings_list = [
        CostSplittingData(
            user_id=cost.user_id,
            accommodation_id=cost.accommodation_id,
            order_id=cost.order_id,
            order_items=cost.order_items,
            share_cost=cost.share_cost,
            payment=cost.payment,
            delivery_fee_split=cost.delivery_fee_split,
            total_split=cost.total_split,
        )
        for cost in cost_splittings
    ]
    
    return AllCostSplittingsResponse(cost_splittings=cost_splittings_list)


@router.get("/{user_id}", response_model=CostSplittingData)
async def fetch_cost_splitting(user_id: str, database: AsyncSession = Depends(fetch_db_session)) -> CostSplittingData:
    """
    Function Overview:
    Fetches details of a specific cost splitting entry based on the provided user ID.

    Function Logic:
    1. Use the user_id parameter to query the database for cost splitting data.
    2. Return the cost splitting data wrapped in a CostSplittingData schema.

    Parameters:
    user_id (str): ID of the user whose cost splitting details are to be fetched.
    database (AsyncSession): Database session dependency to interact with the database.

    Returns:
    CostSplittingData: Details of the requested cost splitting entry.
    """
    query_result = await database.get(CostSplitting, user_id)
    
    if not query_result:
        raise HTTPException(status_code=404, detail=f"Cost splitting entry for user ID '{user_id}' not found.")
    
    return CostSplittingData(
            user_id=query_result.user_id,
            accommodation_id=query_result.accommodation_id,
            order_id=query_result.order_id,
            order_items=query_result.order_items,
            share_cost=query_result.share_cost,
            payment=query_result.payment,
            delivery_fee_split=query_result.delivery_fee_split,
            total_split=query_result.total_split,
        )


@router.post("/add", response_model=CostSplittingsSuccessResponse)
async def add_cost_splitting(request: CostSplittingData, database: AsyncSession = Depends(fetch_db_session)) -> CostSplittingsSuccessResponse:
    """
    Function Overview:
    Adds a new cost splitting entry to the database.

    Function Logic:
    1. Use incoming request data in CostSplittingData schema to create a new cost splitting record.
    2. Insert new cost splitting data into the database.
    3. Return a success message wrapped in a CostSplittingsSuccessResponse schema.

    Parameters:
    request (CostSplittingData): Cost splitting data to be added.
    database (AsyncSession): Database session dependency to interact with the database.

    Returns:
    CostSplittingsSuccessResponse: A response indicating whether the cost splitting entry was added successfully.
    """
    order_query_result = await database.execute(select(CostSplitting).filter(CostSplitting.order_id == request.order_id))
    order_query = order_query_result.scalar_one_or_none()

    if order_query:
        raise HTTPException(status_code=409, detail=f"Cost splitting entry for order ID '{request.order_id}' already exists.")

    add_cost_splitting = CostSplitting(
        user_id=request.user_id,
        accommodation_id=request.accommodation_id,
        order_id=request.order_id,
        order_items=request.order_items,
        share_cost=request.share_cost,
        payment=request.payment,
        delivery_fee_split=request.delivery_fee_split,
        total_split=request.total_split,
    )

    database.add(add_cost_splitting)
    await database.commit()

    return CostSplittingsSuccessResponse(
        action="Add New Cost Splitting Data",
        success=True,
        message=f"Cost splitting data for user ID '{request.user_id}' and order ID '{request.order_id}' added successfully!"
    )


@router.put("/update/{user_id}", response_model=CostSplittingsSuccessResponse)
async def update_cost_splitting(user_id: str, request: CostSplittingData, database: AsyncSession = Depends(fetch_db_session)) -> CostSplittingsSuccessResponse:
    """
    Function Overview:
    Updates details of a specific cost splitting entry in the database.

    Function Logic:
    1. Use the user_id to locate the existing cost splitting entry in the database.
    2. Apply updates based on incoming request data in CostSplittingData schema.
    3. Return a success message wrapped in a CostSplittingsSuccessResponse schema.

    Parameters:
    user_id (str): ID of the user whose cost splitting entry is to be updated.
    request (CostSplittingData): Updated cost splitting data.
    database (AsyncSession): Database session dependency to interact with the database.

    Returns:
    CostSplittingsSuccessResponse: A response indicating whether the update was successful.
    """
    query_result = await database.get(CostSplitting, user_id)

    if not query_result:
        raise HTTPException(status_code=404, detail=f"Cost splitting entry for user ID '{user_id}' not found.")
    
    order_query_result = await database.execute(select(CostSplitting).filter(CostSplitting.order_id == request.order_id))
    order_query = order_query_result.scalar_one_or_none()

    if order_query and order_query.user_id == user_id:
        raise HTTPException(status_code=409, detail=f"Order ID '{request.order_id}' already has an entry for user ID '{order_query.user_id}'.")

    query_result.user_id = request.user_id
    query_result.accommodation_id = request.accommodation_id
    query_result.order_id = request.order_id
    query_result.order_items = request.order_items
    query_result.share_cost = request.share_cost
    query_result.payment = request.payment
    query_result.delivery_fee_split = request.delivery_fee_split
    query_result.total_split = request.total_split

    await database.commit()

    return CostSplittingsSuccessResponse(
        action="Update Cost Splitting Data",
        success=True,
        message=f"Cost splitting data for user ID '{user_id}' updated successfully!"
    )


@router.delete("/delete/{user_id}", response_model=CostSplittingsSuccessResponse)
async def delete_cost_splitting(user_id: str, database: AsyncSession = Depends(fetch_db_session)) -> CostSplittingsSuccessResponse:
    """
    Function Overview:
    Deletes a specific cost splitting entry from the database based on the provided user ID.

    Function Logic:
    1. Use the user_id to locate the cost splitting entry in the database.
    2. Remove the cost splitting entry from the database.
    3. Return a success message wrapped in a CostSplittingsSuccessResponse schema.

    Parameters:
    user_id (str): ID of the user whose cost splitting entry is to be deleted.
    database (AsyncSession): Database session dependency to interact with the database.

    Returns:
    CostSplittingsSuccessResponse: A response indicating whether the deletion was successful.
    """
    query_result = await database.get(CostSplitting, user_id)

    if not query_result:
        raise HTTPException(status_code=404, detail=f"Cost splitting entry for user ID '{user_id}' not found.")

    await database.execute(delete(CostSplitting).filter(CostSplitting.user_id == user_id))
    await database.commit()

    return CostSplittingsSuccessResponse(
        action="Delete Cost Splitting Data",
        success=True,
        message=f"Cost splitting entry for user ID '{user_id}' and order ID '{query_result.order_id}' deleted successfully!"
    )
