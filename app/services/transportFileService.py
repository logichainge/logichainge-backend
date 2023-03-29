from typing import Any
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy import update
from app import models, schemas
from app.schemas.transportFile import TransportFileBase
from app.services import contactService, clientService, employeeService, \
    departmentService, activityService, \
    goodsService, addressService


def get_all_transport_file(db: Session):
    """
    Get all transport_files from the db.
    """

    result =  db.query(models.TransportFile).all()

    return result


def get_all_transport_file_by_status(db: Session, status: str):
    """
    Get all transport files filtered by status from the db.
    """

    all_transport_files_by_status = db.query(models.TransportFile) \
        .filter(models.TransportFile.tr_file_status == status) \
        .all()
    for db_transport_file in all_transport_files_by_status:
        db_transport_file.first_activity = db.query(models.Activity).filter(models.Activity.transport_file_id == db_transport_file.id).order_by(models.Activity.sequence_id.asc()).first()
        db_transport_file.last_activity = db.query(models.Activity).filter(models.Activity.transport_file_id == db_transport_file.id).order_by(models.Activity.sequence_id.desc()).first()

    return all_transport_files_by_status


def get_transport_file(db: Session, id: int):
    """
    Get a transport file by id from the db.
    """

    db_transport_file = db.query(models.TransportFile).filter(models.TransportFile.id == id).first()

    return db_transport_file


def save_transport_file_basic_fields(db: Session, transport_file_in: TransportFileBase, ) -> Any:
    """
    Save a transport file to the db, but excluding nested objects
    """
    transport_file_data = jsonable_encoder(
        transport_file_in,
        exclude={"client", "contact", "department", "employee", "activities"})

    db_transport_file = models.TransportFile(**transport_file_data)

    db.add(db_transport_file)
    db.commit()
    db.refresh(db_transport_file)
    return db_transport_file


def save_transport_file(db: Session, transport_file_in: TransportFileBase, ) -> Any:
    """
    Save a transport file to the db.
    """
    transport_file_data = jsonable_encoder(transport_file_in)
    db_transport_file = models.TransportFile(**transport_file_data)

    db.add(db_transport_file)
    db.commit()
    db.refresh(db_transport_file)
    return db_transport_file


def update_transport_file(db: Session, transport_file_update: TransportFileBase, id: int):
    """
    Update only basic transport_file fields
    """
    tr_file_query = {}
    stmt = (
        update(models.TransportFile)
        .where(models.TransportFile.id == id)
        .values(transport_file_update.dict(
        exclude={
            "client", "contact", "department",
            "employee", "activities"
        }))
    )
    db.execute(stmt)
    db.commit()
    tr_file_query = db.query(models.TransportFile).filter(models.TransportFile.id == id).first()

    return tr_file_query

def mark_transport_file_as_reported(db: Session, id: int):
    """
    Mark the transport file as reported by user as incorrect or incomplete
    """
    stmt = (
        update(models.TransportFile)
        .where(models.TransportFile.id == id)
        .values({"reported" : True})
    )
    db.execute(stmt)
    db.commit()

    return True


def delete_transport_file(db: Session, id: int):
    """
    Delete a transport file from the db.
    """
    transport_file_to_delete = get_transport_file(db, id)
    db.delete(transport_file_to_delete)
    db.commit()
    return transport_file_to_delete
