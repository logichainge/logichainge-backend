from typing import List, Optional

from pydantic import BaseModel
from app import schemas
import datetime


class TransportFileBase(BaseModel):
	"""
	Transport_file base schema
	"""
	tr_file_status: Optional[str]
	display_number: str
	invoice_reference: List[str]
	file_type: str
	equipment_type: str
	modality: str
	service_level: str
	customs: str
 
	attention_required: Optional[bool]
	multi_trip: Optional[bool]
	multi_activity: Optional[bool]
	date_deviation: Optional[bool]
	urgency: Optional[bool]
	late_booking: Optional[bool]
	cost_code: str
	client_id: int
	contact_id: int
	department_id: int
	employee_id: int
	reported: Optional[bool]
	call_before_planning: Optional[bool]
	incoterms: Optional[str]
	certainty: Optional[float]
	reference: Optional[List[str]]
	document_reference: Optional[str]
	
	
	
	class Config:
		orm_mode = True


class TransportFileOut(TransportFileBase):
	"""
	Transport_file OUT schema, inheriting fields from Base class
	"""
	id: int
	client: schemas.ClientOut
	contact: schemas.ContactOut
	department: schemas.DepartmentOut
	employee: schemas.EmployeeOut
	created_at: datetime.datetime