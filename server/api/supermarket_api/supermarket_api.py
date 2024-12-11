from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete
from server.dependencies import fetch_db_session
from server.schemas import ProductData, AllProductsResponse, ProductsSuccessResponse
from server.models import SupermarketProducts

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
    query_result = await database.execute(select(SupermarketProducts))
    products = query_result.scalars().all()

    products_list = [
        ProductData(
            product_id=product.product_id,
            product_name=product.product_name,
            product_category=product.product_category,
            product_price=product.product_price,
            product_stock=product.product_stock
        )
        for product in products
    ]

    return AllProductsResponse(products=products_list)



@router.get("/fetch/{product_id}", response_model=ProductData)
async def fetch_product(product_id: str, database: AsyncSession = Depends(fetch_db_session)) -> ProductData:
    """
    Function Overview:
    Fetches details of a specific product based on provided product ID.

    Function Logic:
    1. Use product_id parameter to query database for product data.
    2. If the data cannot be found, raise a 404 Not Found exception,
       else return product data wrapped in a ProductData schema.

    Parameters:
    database (AsyncSession): Database session dependency to interact with database.
    
    Returns:
    ProductData: A response containing details of requested product conforming to ProductResponse schema.
    """
    query_result = await database.get(SupermarketProducts, product_id)

    if not query_result:
        raise HTTPException(status_code=404, detail=f"Product with ID '{product_id}' not found.")

    return ProductData(
        product_id=query_result.product_id,
        product_name=query_result.product_name,
        product_category=query_result.product_category,
        product_price=query_result.product_price,
        product_stock=query_result.product_stock
    )



@router.put("/update/{product_id}", response_model=ProductsSuccessResponse)
async def update_product(product_id: str, request: ProductData, database: AsyncSession = Depends(fetch_db_session)) -> ProductsSuccessResponse:
    """
    Function Overview:
    Updates details of a specific product in database.

    Function Logic:
    1. Use product_id to locate existing product in database.
    2. If the product cannot be found, raise a 404 Not Found exception.
    3. Check if the requested updates violate uniquness rules for the table,
       raise a 409 Conflict exception if it is violated..
    4. Apply updates based on incoming request data in ProductData schema.
    5. Return a success message wrapped in a ProductsSuccessResponse schema.

    Parameters:
    request (ProductData): New product data to be updated.
    database (AsyncSession): Database session dependency to interact with database.

    Returns:
    ProductsSuccessResponse: A response indicating whether update was successful conforming to ProductsSuccessResponse schema.
    """
    query_result = await database.get(SupermarketProducts, product_id)

    if not query_result:
        raise HTTPException(status_code=404, detail=f"Product with ID '{product_id}' not found.")
    
    result = await database.execute(select(SupermarketProducts).filter(SupermarketProducts.product_name == request.product_name))
    product_query_result = result.scalar_one_or_none()
    id_query_result = await database.get(SupermarketProducts, request.product_id)

    if product_query_result and product_query_result.product_id != product_id:
        raise HTTPException(status_code=409, detail=f"Product '{request.product_name}' already exists with ID '{product_query_result.product_id}'.")
    if id_query_result and id_query_result.product_id != product_id:
        raise HTTPException(status_code=409, detail=f"Product ID '{request.product_id}' already exists for product '{id_query_result.product_name}'.")

    if query_result.product_id == request.product_id:
        success_response = ProductsSuccessResponse(
        action="Update Product Data",
        success=True,
        message=f"Product information for ID '{product_id}' updated in database successfully!"
    )
    else:
        success_response = ProductsSuccessResponse(
        action="Update Product Data",
        success=True,
        message=f"Product information for ID '{product_id}' updated in database successfully, new product ID is '{request.product_id}'."
    )

    query_result.product_id = request.product_id
    query_result.product_name = request.product_name
    query_result.product_category = request.product_category
    query_result.product_price = request.product_price
    query_result.product_stock = request.product_stock

    await database.commit()

    return success_response



@router.post("/add", response_model=ProductsSuccessResponse)
async def add_product(request: ProductData, database: AsyncSession = Depends(fetch_db_session)) -> ProductsSuccessResponse:
    """
    Function Overview:
    Adds a new product to database.

    Function Logic:
    1. Check if the product in the incoming request already exits in the table, or if its requested ID is being used.
    2. If it exists, raise a 409 Conflict exception,
       else use incoming request data in ProductData schema to create a new product record.
    3. Insert new product data into database.
    4. Return a success message wrapped in a ProductsSuccessResponse schema.

    Parameters:
    request (ProductData): Product data to be added.
    database (AsyncSession): Database session dependency to interact with database.

    Returns:
    ProductsSuccessResponse: A response indicating whether product was added successfully conforming to ProductsSuccessResponse schema.
    """
    id_query_result = await database.get(SupermarketProducts, request.product_id)
    query_result = await database.execute(select(SupermarketProducts).filter(SupermarketProducts.product_name == request.product_name))
    product_query_result = query_result.scalar_one_or_none()

    if id_query_result:
        raise HTTPException(status_code=409, detail=f"Product with ID '{request.product_id}' already exists.")
    elif product_query_result:
        raise HTTPException(status_code=409, detail=f"Product with name '{request.product_name}' already exists.")
    
    add_product = SupermarketProducts(
        product_id=request.product_id,
        product_name=request.product_name,
        product_category=request.product_category,
        product_price=request.product_price,
        product_stock=request.product_stock
    )

    database.add(add_product)
    await database.commit()

    return ProductsSuccessResponse(
        action="Add New Product Data",
        success=True,
        message=f"Product with ID '{request.product_id}' and name '{request.product_name}' added to database successfully!"
    )



@router.delete("/delete/{product_id}", response_model=ProductsSuccessResponse)
async def delete_product(product_id: str, database: AsyncSession = Depends(fetch_db_session)) -> ProductsSuccessResponse:
    """
    Function Overview:
    Deletes a specific product from database based on provided product ID.

    Function Logic:
    1. Use product_id to locate product in database.
    2. If the product cannot be located, raise a 404 Not Found exception,
       else remove product from database.
    3. Return a success message wrapped in a ProductsSuccessResponse schema.

    Parameters:
    product_id (int): ID of the product to be deleted.
    database (AsyncSession): Database session dependency to interact with database.

    Returns:
    ProductsSuccessResponse: A response indicating whether deletion was successful conforming to ProductsSuccessResponse schema.
    """
    query_result = await database.get(SupermarketProducts, product_id)

    if not query_result:
        raise HTTPException(status_code=404, detail=f"Product ID '{product_id}' not found.")

    await database.execute(delete(SupermarketProducts).filter(SupermarketProducts.product_id == product_id))
    await database.commit()

    return ProductsSuccessResponse(
        action="Delete Product Data",
        success=True,
        message=f"Product with ID {product_id} and name '{query_result.product_name}' deleted from database successfully!"
    )
