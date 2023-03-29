from pydantic import BaseModel
import datetime
from typing import List, Optional
from uuid import UUID


class AttachmentBase(BaseModel):
	"""
	Attachment BASE schema
	"""
	url: str
	tr_file_id: int

	
	class Config:
		orm_mode = True


class AttachmentOut(AttachmentBase):
	"""
	Attachment OUT schema, inheriting fields from Base class
	"""
	id: int
	created_at: datetime.datetime
	
	