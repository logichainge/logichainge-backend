from fastapi import Depends, APIRouter, Response, status, HTTPException, Header
from sqlalchemy.orm import Session
from app.database.database import get_db
from typing import List, Any
from app import schemas
from app.services import transportFileService, activityService
from sqlalchemy import exc
from fastapi.encoders import jsonable_encoder

# Defining the router
router = APIRouter(
    prefix="/transport_files",
    tags=["transport_file"],
    responses={404: {"description": "Not Found"}},
)


def not_found_exception(id):
    """
    Not founds with specific ID exception
    """
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Transport file with id= {id} not found"
    )

def no_activities_found_exception(id):
    """
    Not founds with specific ID exception
    """
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No activities found for transport file with id= {id} "
    )


@router.get("/")
def get_all_transport_files(db: Session = Depends(get_db)):
	all_files = transportFileService.get_all_transport_file(db)
	return jsonable_encoder(all_files)


@router.get("/get_by_status/{status}", response_model=List[schemas.TransportFileOut])
def get_all_transport_files_by_status(status: str, db: Session = Depends(get_db)):
    """
    Get all transport_files by their status (tr_file_status)
    """

    all_files_by_status = transportFileService.get_all_transport_file_by_status(db, status)
    return all_files_by_status


@router.get("/{id}", response_model=schemas.TransportFileOut)
def get_transport_file(id: int, db: Session = Depends(get_db), ):
    """
    Get a transport_file by its ID
    """

    db_transport_file = transportFileService.get_transport_file(db, id)
    if not db_transport_file:
        raise not_found_exception(id)

    return db_transport_file

@router.get("/{id}/activities", response_model=List[schemas.ActivityOut])
def get_transport_file(id: int, db: Session = Depends(get_db), ):
    """
    Get a transport_file by its ID
    """

    activities = activityService.get_activities_for_transport_file(db = db, transport_file_id=id)
    if not activities:
        raise no_activities_found_exception(id)

    return activities

@router.post("/", response_model=schemas.TransportFileOut, status_code=status.HTTP_201_CREATED)
def create_transport_file(transport_file: schemas.TransportFileBase, db: Session = Depends(get_db), ):
    """
    Create transport_file with basic fields
    """
    try:
        db_transport_file = transportFileService.save_transport_file_basic_fields(db, transport_file)
    except exc.IntegrityError as e:
        print(e.orig)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid input")

    return db_transport_file

@router.put("/{id}", response_model=schemas.TransportFileOut)
def update_transport_file(*,
                          id: int,
                          db: Session = Depends(get_db),
                          transport_file_update: schemas.TransportFileBase,
                          ) -> Any:
    """
    Update a specific transport_file
    """
    db_transport_file = transportFileService.get_transport_file(db, id)

    if not db_transport_file:
        raise not_found_exception(id)

    try:
        db_transport_file_updated = transportFileService.update_transport_file(db, transport_file_update, id)
    except (exc.IntegrityError) as e:
        print(e.orig)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid input")

    return db_transport_file_updated

@router.post("/{id}/report", status_code=status.HTTP_204_NO_CONTENT)
def update_transport_file(*,
                          id: int,
                          db: Session = Depends(get_db),
                          ) -> Any:
    """
    Report a specific transport_file as incorrect or incomplete
    """
    db_transport_file = transportFileService.get_transport_file(db, id)

    if not db_transport_file:
        raise not_found_exception(id)

    try:
        transportFileService.mark_transport_file_as_reported(db, id)
    except (exc.IntegrityError) as e:
        print(e.orig)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid input")

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transport_file(*, db: Session = Depends(get_db), id: int, ):
    """
    Delete a specific transport_file
    """
    db_transport_file = transportFileService.get_transport_file(db, id)

    if not db_transport_file:
        raise not_found_exception(id)
    transportFileService.delete_transport_file(db, id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
