from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete
from server.dependencies import fetch_db_session
from server.schemas import OrderData, AllOrdersResponse, OrdersSuccessResponse
from server.models import Orders

router = APIRouter()



@router.get("/all", response_model=AllOrdersResponse)
async def fetch_all_orders(database: AsyncSession = Depends(fetch_db_session)) -> AllOrdersResponse:
    """
    Function Overview:
    Fetches all shared orders from the database.

    Function Logic:
    1. Use database session to query the Orders table.
    2. Convert each Orders object to OrderData schema.
    3. Return the list of shared orders wrapped in an AllOrdersResponse schema.

    Parameters:
    database (AsyncSession): Database session dependency to interact with the database.

    Returns:
    AllOrdersResponse: A response containing a list of all shared orders conforming to the schema.
    """
    query_result = await database.execute(select(Orders))
    orders = query_result.scalars().all()

    orders_list = [
        OrderData(
            order_id=order.order_id,
            accommodation_id=order.accommodation_id,
            creation_date=order.creation_date,
            order_status=order.order_status,
            item_cost=order.items_cost,
            delivery_fee=order.delivery_fee,
            order_total=order.order_total
        )
        for order in orders
    ]

    return AllOrdersResponse(orders=orders_list)


@router.get("/{order_id}", response_model=OrderData)
async def fetch_order(order_id: str, database: AsyncSession = Depends(fetch_db_session)) -> OrderData:
    """
    Function Overview:
    Fetches details of a specific shared order by its ID.

    Function Logic:
    1. Use the order_id parameter to query the database for the shared order.
    2. If the shared order does not exist, raise a 404 Not Found exception.
    3. Return the shared order details wrapped in a OrderData schema.

    Parameters:
    order_id (str): Unique identifier of the shared order.
    database (AsyncSession): Database session dependency to interact with the database.

    Returns:
    OrderData: A response containing the details of the shared order.
    """
    query_result = await database.get(Orders, order_id)

    if not query_result:
        raise HTTPException(status_code=404, detail=f"Order with ID '{order_id}' not found.")

    return OrderData(
        order_id=query_result.order_id,
        accommodation_id=query_result.accommodation_id,
        creation_date=query_result.creation_date,
        order_status=query_result.order_status,
        item_cost=query_result.items_cost,
        delivery_fee=query_result.delivery_fee,
        order_total=query_result.order_total
    )


@router.put("/update/{order_id}", response_model=OrdersSuccessResponse)
async def update_order(order_id: str, request: OrderData, database: AsyncSession = Depends(fetch_db_session)) -> OrdersSuccessResponse:
    """
    Function Overview:
    Updates the details of a specific shared order.

    Function Logic:
    1. Use the order_id to locate the shared order in the database.
    2. If the shared order does not exist, raise a 404 Not Found exception.
    3. Update the shared order with the new details provided in the request.
    4. Commit the changes to the database.
    5. Return a success message wrapped in a OrdersSuccessResponse schema.

    Parameters:
    order_id (str): Unique identifier of the shared order to update.
    request (OrderData): New data to update the shared order with.
    database (AsyncSession): Database session dependency to interact with the database.

    Returns:
    OrdersSuccessResponse: A response indicating the success of the update operation.
    """
    query_result = await database.get(Orders, order_id)

    if not query_result:
        raise HTTPException(status_code=404, detail=f"Order with ID '{order_id}' not found.")
    
    id_query_result = await database.get(Orders, request.order_id)
    if id_query_result and id_query_result.order_id != order_id:
        raise HTTPException(status_code=409, detail=f"Order ID '{request.order_id}' already exists.")

    if query_result.order_id == request.order_id:
        success_response = OrdersSuccessResponse(
        action="Update Order Data",
        success=True,
        message=f"Order information for ID '{order_id}' updated in database successfully!"
    )
    else:
        success_response = OrdersSuccessResponse(
        action="Update Order Data",
        success=True,
        message=f"Order information for ID '{order_id}' updated in database successfully, new order ID is '{request.order_id}'."
    )

    query_result.order_id = request.order_id
    query_result.accommodation_id = request.accommodation_id
    query_result.creation_date = request.creation_date
    query_result.order_status = request.order_status
    query_result.items_cost = request.items_cost
    query_result.delivery_fee = request.delivery_fee
    query_result.order_total = request.order_total

    await database.commit()

    return success_response


@router.post("/add", response_model=OrdersSuccessResponse)
async def add_order(request: OrderData, database: AsyncSession = Depends(fetch_db_session)) -> OrdersSuccessResponse:
    """
    Function Overview:
    Adds a new shared order to the database.

    Function Logic:
    1. Check if a shared order with the same ID already exists in the database.
    2. If it exists, raise a 409 Conflict exception.
    3. Create a new shared order with the data provided in the request.
    4. Add the shared order to the database and commit the transaction.
    5. Return a success message wrapped in a OrdersSuccessResponse schema.

    Parameters:
    request (OrderData): Data for the new shared order to be added.
    database (AsyncSession): Database session dependency to interact with the database.

    Returns:
    OrdersSuccessResponse: A response indicating the success of the add operation.
    """
    query_result = await database.get(Orders, request.order_id)

    if query_result:
        raise HTTPException(status_code=409, detail=f"Order with ID '{request.order_id}' already exists.")

    add_order = Orders(
        order_id=request.order_id,
        accommodation_id=request.accommodation_id,
        creation_date=request.creation_date,
        order_status=request.order_status,
        items_cost=request.order_status,
        delivery_fee=request.delivery_fee,
        order_total=request.order_total
    )
    
    database.add(add_order)
    await database.commit()

    return OrdersSuccessResponse(
        action="Add New Order Data",
        success=True,
        message=f"Order with ID '{request.order_id}' added successfully!"
    )


@router.delete("/delete/{order_id}", response_model=OrdersSuccessResponse)
async def delete_order(order_id: str, database: AsyncSession = Depends(fetch_db_session)) -> OrdersSuccessResponse:
    """
    Function Overview:
    Deletes a shared order from the database.

    Function Logic:
    1. Use the order_id to locate the shared order in the database.
    2. If the shared order does not exist, raise a 404 Not Found exception.
    3. Remove the shared order from the database and commit the transaction.
    4. Return a success message wrapped in a OrdersSuccessResponse schema.

    Parameters:
    order_id (str): Unique identifier of the shared order to delete.
    database (AsyncSession): Database session dependency to interact with the database.

    Returns:
    OrdersSuccessResponse: A response indicating the success of the delete operation.
    """
    query_result = await database.get(Orders, order_id)

    if not query_result:
        raise HTTPException(status_code=404, detail=f"Order with ID '{order_id}' not found.")

    await database.execute(delete(Orders).filter(Orders.order_id == order_id))
    await database.commit()

    return OrdersSuccessResponse(
        action="Delete Order Data",
        success=True,
        message=f"Order with ID '{order_id}' deleted successfully!"
    )
