from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional


class UserBase(BaseModel):
	"""
	User BASE schema
	"""
	username: str
	email: str
	disabled: bool
	full_name: Optional[str]
	first_login: Optional[bool]
	password_reset_needed: Optional[bool]
	is_admin: Optional[bool]
	
	class Config:
		orm_mode = True
	

class UserOut(UserBase):
	"""
	Client OUT schema, inheriting fields from Base class
	"""
	id: int
	created_at: datetime
	
class UserIn(UserBase):
	password: str

class Pass(BaseModel):
	password: str
