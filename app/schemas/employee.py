from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel
from app import schemas


class EmployeeBase(BaseModel):
	"""
	Employee BASE schema
	"""
	# transport_file_id: int
	name: str
	client_id: Optional[int]
	
	class Config:
		orm_mode = True


class EmployeeOut(EmployeeBase):
	"""
	Employee OUT schema, inheriting fields from Base class
	"""
	id: int
	created_at: datetime
	