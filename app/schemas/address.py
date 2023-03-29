from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel


class AddressBase(BaseModel):
	"""
	Address BASE schema
	"""
	name: List[str]
	street_1: List[str]
	street_2: Optional[List[str]]
	street_3: Optional[List[str]]
	zipcode: List[str]
	city: List[str]
	country: List[str]
	latitude: float
	longitude: float
	
	class Config:
		orm_mode = True


class AddressOut(AddressBase):
	"""
	Address OUT schema, inheriting fields from Base class
	"""
	id: int
	created_at: datetime
	