from typing import List, Optional
from app import schemas
from pydantic import BaseModel
from datetime import datetime


class ActivityBase(BaseModel):
	"""
	Activity BASE schema
	"""
	transport_file_id: int
	sequence_id: int
	activity_reference: List[str]
	activity_type: str
	address_id: int
	date: List[str]
	time_prefix: str
	time_1: List[str]
	time_2: List[str]
	instructions: Optional[str]
	contact_id: int
	
	class Config:
		orm_mode = True


class ActivityOut(ActivityBase):
	"""
	Activity OUT schema, inheriting fields from Base class
	"""
	id: int
	address: schemas.AddressOut
	contact: schemas.ContactOut
	created_at: datetime