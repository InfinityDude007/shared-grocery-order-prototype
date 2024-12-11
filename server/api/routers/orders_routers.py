from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete
from server.dependencies import fetch_db_session
from server.schemas import SharedOrderData, AllSharedOrdersResponse, SuccessResponse
from server.models import SharedOrder

router = APIRouter()



@router.get("/all", response_model=AllSharedOrdersResponse)
async def fetch_all_orders(database: AsyncSession = Depends(fetch_db_session)) -> AllSharedOrdersResponse:
    """
    Function Overview:
    Fetches all shared orders from the database.

    Function Logic:
    1. Use database session to query the SharedOrder table.
    2. Convert each SharedOrder object to SharedOrderData schema.
    3. Return the list of shared orders wrapped in an AllSharedOrdersResponse schema.

    Parameters:
    database (AsyncSession): Database session dependency to interact with the database.

    Returns:
    AllSharedOrdersResponse: A response containing a list of all shared orders conforming to the schema.
    """
    query_result = await database.execute(select(SharedOrder))
    orders = query_result.scalars().all()

    orders_list = [
        SharedOrderData(
            order_id=order.order_id,
            group_id=order.group_id,
            creation_date=order.creation_date,
            order_status=order.order_status,
            delivery_fee=order.delivery_fee
        )
        for order in orders
    ]

    return AllSharedOrdersResponse(orders=orders_list)


@router.get("/{order_id}", response_model=SharedOrderData)
async def fetch_order(order_id: str, database: AsyncSession = Depends(fetch_db_session)) -> SharedOrderData:
    """
    Function Overview:
    Fetches details of a specific shared order by its ID.

    Function Logic:
    1. Use the order_id parameter to query the database for the shared order.
    2. If the shared order does not exist, raise a 404 Not Found exception.
    3. Return the shared order details wrapped in a SharedOrderData schema.

    Parameters:
    order_id (str): Unique identifier of the shared order.
    database (AsyncSession): Database session dependency to interact with the database.

    Returns:
    SharedOrderData: A response containing the details of the shared order.
    """
    query_result = await database.get(SharedOrder, order_id)

    if not query_result:
        raise HTTPException(status_code=404, detail=f"Order with ID '{order_id}' not found.")

    return SharedOrderData(
        order_id=query_result.order_id,
        group_id=query_result.group_id,
        creation_date=query_result.creation_date,
        order_status=query_result.order_status,
        delivery_fee=query_result.delivery_fee
    )


@router.put("/update/{order_id}", response_model=SuccessResponse)
async def update_order(order_id: str, request: SharedOrderData, database: AsyncSession = Depends(fetch_db_session)) -> SuccessResponse:
    """
    Function Overview:
    Updates the details of a specific shared order.

    Function Logic:
    1. Use the order_id to locate the shared order in the database.
    2. If the shared order does not exist, raise a 404 Not Found exception.
    3. Update the shared order with the new details provided in the request.
    4. Commit the changes to the database.
    5. Return a success message wrapped in a SuccessResponse schema.

    Parameters:
    order_id (str): Unique identifier of the shared order to update.
    request (SharedOrderData): New data to update the shared order with.
    database (AsyncSession): Database session dependency to interact with the database.

    Returns:
    SuccessResponse: A response indicating the success of the update operation.
    """
    query_result = await database.get(SharedOrder, order_id)

    if not query_result:
        raise HTTPException(status_code=404, detail=f"Order with ID '{order_id}' not found.")

    query_result.group_id = request.group_id
    query_result.creation_date = request.creation_date
    query_result.order_status = request.order_status
    query_result.delivery_fee = request.delivery_fee

    await database.commit()

    return SuccessResponse(
        action="Update Order Data",
        success=True,
        message=f"Order with ID '{order_id}' updated successfully!"
    )


@router.post("/add", response_model=SuccessResponse)
async def add_order(request: SharedOrderData, database: AsyncSession = Depends(fetch_db_session)) -> SuccessResponse:
    """
    Function Overview:
    Adds a new shared order to the database.

    Function Logic:
    1. Check if a shared order with the same ID already exists in the database.
    2. If it exists, raise a 409 Conflict exception.
    3. Create a new shared order with the data provided in the request.
    4. Add the shared order to the database and commit the transaction.
    5. Return a success message wrapped in a SuccessResponse schema.

    Parameters:
    request (SharedOrderData): Data for the new shared order to be added.
    database (AsyncSession): Database session dependency to interact with the database.

    Returns:
    SuccessResponse: A response indicating the success of the add operation.
    """
    existing_order = await database.get(SharedOrder, request.order_id)

    if existing_order:
        raise HTTPException(status_code=409, detail=f"Order with ID '{request.order_id}' already exists.")

    new_order = SharedOrder(
        order_id=request.order_id,
        group_id=request.group_id,
        creation_date=request.creation_date,
        order_status=request.order_status,
        delivery_fee=request.delivery_fee
    )

    database.add(new_order)
    await database.commit()

    return SuccessResponse(
        action="Add New Order",
        success=True,
        message=f"Order with ID '{request.order_id}' added successfully!"
    )


@router.delete("/delete/{order_id}", response_model=SuccessResponse)
async def delete_order(order_id: str, database: AsyncSession = Depends(fetch_db_session)) -> SuccessResponse:
    """
    Function Overview:
    Deletes a shared order from the database.

    Function Logic:
    1. Use the order_id to locate the shared order in the database.
    2. If the shared order does not exist, raise a 404 Not Found exception.
    3. Remove the shared order from the database and commit the transaction.
    4. Return a success message wrapped in a SuccessResponse schema.

    Parameters:
    order_id (str): Unique identifier of the shared order to delete.
    database (AsyncSession): Database session dependency to interact with the database.

    Returns:
    SuccessResponse: A response indicating the success of the delete operation.
    """
    query_result = await database.get(SharedOrder, order_id)

    if not query_result:
        raise HTTPException(status_code=404, detail=f"Order with ID '{order_id}' not found.")

    await database.execute(delete(SharedOrder).filter(SharedOrder.order_id == order_id))
    await database.commit()

    return SuccessResponse(
        action="Delete Order",
        success=True,
        message=f"Order with ID '{order_id}' deleted successfully!"
    )
