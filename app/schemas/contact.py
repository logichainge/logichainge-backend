from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr
from app import schemas


class ContactBase(BaseModel):
	"""
	Contact BASE schema
	"""
	# transport_file_id: int
	client_id: Optional[int]
	initials: str
	name: str
	surname_prefix: Optional[str]
	surname: str
	phone: List[str]
	mobile: List[str]
	email: List[str]
	
	class Config:
		orm_mode = True


class ContactOut(ContactBase):
	"""
	Contact OUT schema, inheriting fields from Base class
	"""
	id: int
	created_at: datetime
	