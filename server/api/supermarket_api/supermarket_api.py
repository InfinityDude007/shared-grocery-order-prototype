from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Any
from server.dependencies import fetch_db_session

router = APIRouter()



@router.get("/products", response_model=List[Dict[str, Any]])
async def fetch_all_products(database: AsyncSession = Depends(fetch_db_session)) -> List[Dict[str, Any]]:

    # function logic to be added here

    products_list = [
        {
            "product_id": "123",
            "product_name": "Tomato Sauce",
            "product_price": 5,
            "product_stock": 15
        },
        {
            "product_id": "456",
            "product_name": "Barbeque Sauce",
            "product_price": 7,
            "product_stock": 10,
        }
    ]
    return products_list



@router.get("/products/{product_id}", response_model=Dict[str, Any])
async def fetch_product(database: AsyncSession = Depends(fetch_db_session)) -> Dict[str, Any]:

    # function logic to be added here

    product = {
            "product_id": "999",
            "product_name": "Tissues",
            "product_price": 20,
            "product_stock": 18
        }
    return product



@router.put("/products/update/{product_id}", response_model=str)
async def update_product(request: Dict, product_id: int, database: AsyncSession = Depends(fetch_db_session)) -> str:

    # function logic to be added here

    return f"Product information for ID {product_id} updated in database successfully!"



@router.post("/products/add/{product_id}", response_model=str)
async def add_product(request: Dict, product_id: int, database: AsyncSession = Depends(fetch_db_session)) -> str:

    # function logic to be added here

    return f"Product with ID {product_id} added to database successfully!"



@router.delete("/products/delete/{product_id}", response_model=str)
async def delete_product(product_id: int, database: AsyncSession = Depends(fetch_db_session)) -> str:

    # function logic to be added here

    return f"Product with ID {product_id} deleted from database successfully!"
