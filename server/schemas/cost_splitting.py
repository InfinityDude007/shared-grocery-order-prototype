from pydantic import BaseModel
from typing import List, Tuple, Literal


# schema for the details related to a single cost splitting entry
class CostSplittingData(BaseModel):
    user_id: str
    accomodation_id: str
    order_id: str
    order_items: List[Tuple[str, int]]
    share_cost: float
    payment: bool
    delivery_fee_split: float
    total_split: float


# schema for the list of all cost splitting entries
class AllCostSplittingsResponse(BaseModel):
    cost_splittings: List[CostSplittingData]


# schema for showing the outcome of a put, post, or delete request for cost splitting data
class CostSplittingsSuccessResponse(BaseModel):
    action: Literal['Update Cost Splitting Data', 'Add New Cost Splitting Data', 'Delete Cost Splitting Data']
    success: bool
    message: str
