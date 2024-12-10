from pydantic import BaseModel
from typing import List, Literal


# schema for the details related to an individual product
class ProductData(BaseModel):
    product_id: str
    product_name: str
    product_category: str
    product_price: float
    product_stock: int


# schema for the list of all product details available
class AllProductsResponse(BaseModel):
    products: List[ProductData]


# schema for showing the outcome of a put, post or delete request
class SuccessResponse(BaseModel):
    action: Literal['Update Product Data', 'Add New Product Data', 'Delete Product Data']
    success: bool
    message: str
