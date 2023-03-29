from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel
from app import schemas


class DepartmentBase(BaseModel):
	"""
	Department BASE schema
	"""
	client_id: Optional[int]
	name: str
	
	class Config:
		orm_mode = True


class DepartmentOut(DepartmentBase):
	"""
	Department OUT schema, inheriting fields from Base class
	"""
	id: int
	created_at: datetime
	