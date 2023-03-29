from typing import TypeVar, Generic, Type, Any, Optional, List, Union, Dict

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.database.database import Base
from pydantic import BaseModel

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class DefaultService(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
	def __init__(self, model: Type[ModelType]):
		"""
		Data Service class with default methods to persists(Create, Read, Update, Delete (CRUD))
		objects to the database.

		**Parameters**

		* `model`: A SQLAlchemy model class
		* `schema`: A Pydantic model (schema) class
		"""
		self.model = model
	
	def get(self, db: Session, id: Any) -> Optional[ModelType]:
		"""
		Get the specified object by its ID from the Database.
		"""
		
		return db.query(self.model).filter(self.model.id == id).first()
	
	def get_multiple(
			self, db: Session, *, skip: int = 0, limit: int = 100
	) -> List[ModelType]:
		"""
		Get all the specified objects from the Database.
		(Optional skip and limit parameters).
		"""
		return db.query(self.model).offset(skip).limit(limit).all()
	
	def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
		"""
		Save a new entry of the specified object to the Database.
		(Have to provide an object that will be saved.)
		"""
		obj_in_data = jsonable_encoder(obj_in)
		db_obj = self.model(**obj_in_data)  # type: ignore
		db.add(db_obj)
		db.commit()
		db.refresh(db_obj)
		return db_obj
	
	def update(self, db: Session, obj_in, id) -> Any:
		"""
		Update an entry of the specified object in the Database.
		
		(Have to provide the updated object,
		And the ID of the object its replacing.)
		"""
		obj_db_query = db.query(self.model).filter(self.model.id == id)
		
		obj_db_query.update(obj_in.dict())
		db.commit()
		
		return obj_db_query.first()
	
	def delete(self, db: Session, *, id: int) -> ModelType:
		"""
		Delete an entry of the specified object from the Database.
		(Have to provide the id of the object that will be deleted.)
		"""
		obj = db.query(self.model).get(id)
		db.delete(obj)
		db.commit()
		return obj
