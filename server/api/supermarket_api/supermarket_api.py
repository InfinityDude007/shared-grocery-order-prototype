from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Any
from server.dependencies import fetch_db_session
from server.schemas.supermarket_api import ProductData, AllProductsResponse, SuccessResponse

router = APIRouter()



@router.get("/products", response_model=AllProductsResponse)
async def fetch_all_products(database: AsyncSession = Depends(fetch_db_session)) -> AllProductsResponse:
    """
    Function Overview:
    Fetches all available products from database.

    Function Logic:
    1. Use database session to query supermarket products table.
    2. Return fetched products as list of ProductData schemas.
    3. Return list of products wrapped in an AllProductsResponse schema.

    Parameters:
    database (AsyncSession): Database session dependency to interact with the database.

    Returns:
    AllProductsResponse: A response containing a list of all available products conforming to AllProductsResponse schema.
    """

    # function logic to be added here

    # return mock data for testing route
    return AllProductsResponse(
        products=[
            ProductData(
                product_id="123",
                product_name="Tomato Sauce",
                product_price=5,
                product_stock=15
                ),
            ProductData(
                product_id="456",
                product_name="Barbeque Sauce",
                product_price=7,
                product_stock=10,
            )
        ]
    )



@router.get("/products/{product_id}", response_model=ProductData)
async def fetch_product(database: AsyncSession = Depends(fetch_db_session)) -> ProductData:
    """
    Function Overview:
    Fetches details of a specific product based on provided product ID.

    Function Logic:
    1. Use product_id parameter to query database for product data.
    2. Return product data wrapped in a ProductData schema.

    Parameters:
    database (AsyncSession): Database session dependency to interact with database.
    
    Returns:
    ProductData: A response containing details of requested product conforming to ProductResponse schema.
    """

    # function logic to be added here

    # return mock data for testing route
    return ProductData(
        product_id="999",
        product_name="Tissues",
        product_price=20,
        product_stock=18
    )



@router.put("/products/update/{product_id}", response_model=SuccessResponse)
async def update_product(request: ProductData, product_id: int, database: AsyncSession = Depends(fetch_db_session)) -> SuccessResponse:
    """
    Function Overview:
    Updates details of a specific product in database.

    Function Logic:
    1. Use product_id to locate existing product in database.
    2. Apply updates based on incoming request data in ProductData schema.
    4. Return a success message wrapped in a SuccessResponse schema.

    Parameters:
    request (ProductData): New product data to be updated.
    product_id (int): ID of the product to be updated.
    database (AsyncSession): Database session dependency to interact with database.

    Returns:
    SuccessResponse: A response indicating whether update was successful conforming to SuccessResponse schema.
    """

    # function logic to be added here

    # return mock data for testing route
    return SuccessResponse(
        action="Update Product Data",
        success=True,
        message=f"Product information for ID {product_id} updated in database successfully!"
    )



@router.post("/products/add/{product_id}", response_model=SuccessResponse)
async def add_product(request: ProductData, product_id: int, database: AsyncSession = Depends(fetch_db_session)) -> SuccessResponse:
    """
    Function Overview:
    Adds a new product to database.

    Function Logic:
    1. Use incoming request data in ProductData schema to create a new product record.
    2. Insert new product data into database.
    3. Return a success message wrapped in a SuccessResponse schema.

    Parameters:
    request (ProductData): Product data to be added.
    product_id (int): ID for the new product.
    database (AsyncSession): Database session dependency to interact with database.

    Returns:
    SuccessResponse: A response indicating whether product was added successfully conforming to SuccessResponse schema.
    """

    # function logic to be added here

    # return mock data for testing route
    return SuccessResponse(
        action="Add New Product Data",
        success=True,
        message=f"Product with ID {product_id} added to database successfully!"
    )



@router.delete("/products/delete/{product_id}", response_model=SuccessResponse)
async def delete_product(product_id: int, database: AsyncSession = Depends(fetch_db_session)) -> SuccessResponse:
    """
    Function Overview:
    Deletes a specific product from database based on provided product ID.

    Function Logic:
    1. Use product_id to locate product in database.
    2. Remove product from database.
    3. Return a success message wrapped in a SuccessResponse schema.

    Parameters:
    product_id (int): ID of the product to be deleted.
    database (AsyncSession): Database session dependency to interact with database.

    Returns:
    SuccessResponse: A response indicating whether deletion was successful conforming to SuccessResponse schema.
    """

    # function logic to be added here

    # return mock data for testing route
    return SuccessResponse(
        action="Delete Product Data",
        success=True,
        message=f"Product with ID {product_id} deleted from database successfully!"
    )
