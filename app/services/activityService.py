from typing import List, Generic, Type, Any
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app import models
from app.schemas.activity import ActivityBase
from sqlalchemy import exc
from pydantic import errors
from app.models import Activity


def get_all_activity(db: Session):
	"""
	Get all activity items from the db.
	"""
	all_activities = db.query(models.Activity).all()
	return all_activities

def  get_activities_for_transport_file(db: Session, transport_file_id: int):
    """
    Get all activities for a transport file by id from the db.
    """

    activities_for_trasnport_file = db.query(models.Activity).filter(models.Activity.transport_file_id == transport_file_id).order_by(models.Activity.sequence_id.asc()).all()

    return activities_for_trasnport_file

def get_activity(db: Session, id: int):
	"""
	Get an activity item by ID from the db.
	"""
	return db.query(models.Activity).filter(models.Activity.id == id).first()


def save_activity(
		db: Session,
		activity_in: ActivityBase
) -> Any:
	"""
	Save new activity item to the db.
	"""
	activity_data = jsonable_encoder(activity_in)
	db_activity = models.Activity(**activity_data)

	db.add(db_activity)
	db.commit()
	db.refresh(db_activity)

	return db_activity
	
	
def save_activity_basic_fields(
		db: Session,
		activity_in: ActivityBase
) -> Any:
	"""
	Save new activity item to the db from parent transport_file, but excluding some fields.
	"""
	activity_data = jsonable_encoder(activity_in, exclude={"activity_reference", "address", "goods"})
	db_activity = models.Activity(**activity_data)

	db.add(db_activity)
	db.commit()
	db.refresh(db_activity)

	return db_activity


def update_activity(db: Session, activity_update: ActivityBase, id: int) -> Any:
	"""
	Update an activity item in the db.
	"""
	activity_query = db.query(models.Activity).filter(models.Activity.id == id)
	
	activity_query.update(activity_update.dict())
	db.commit()
	
	return activity_query.first()


def delete_activity(db: Session, id: int) -> Any:
	"""
	Delete an activity item form the db.
	"""
	activity_to_delete = get_activity(db, id)
	db.delete(activity_to_delete)
	db.commit()
	return activity_to_delete

