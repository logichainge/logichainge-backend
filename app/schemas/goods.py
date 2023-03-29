from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel


class GoodsBase(BaseModel):
    """
    Goods Base schema
    """

    activity_id: int
    unit_type: List[str]
    stackable: bool
    quantity: List[str]
    description: List[str]
    loading_meters: Optional[List[str]]
    net_weight: Optional[List[str]]
    gross_weight: Optional[List[str]]
    dangerous_goods: Optional[bool]
    dg_class: str
    dg_product_group: str
    dg_un_code: str
    dg_technical_name: str
    size: List[str]
    volume_cbm: List[str]
    

    class Config:
        orm_mode = True
    
    
class GoodsOut(GoodsBase):
    """
    Goods OUT schema, inheriting fields from IN class
    """
    id: int
    created_at: datetime
    
    
    