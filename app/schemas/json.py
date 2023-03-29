from typing import List, Optional, Any
from app import schemas
from pydantic import BaseModel
from datetime import datetime


class JsonBase(BaseModel):
	json_data:Any