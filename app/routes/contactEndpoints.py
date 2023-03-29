from fastapi import Depends, APIRouter, Response, status, HTTPException
from sqlalchemy import exc
from sqlalchemy.orm import Session
from app.database.database import get_db
from typing import List, Any
from app import schemas
from app.services.contactService import contactService

# Defining the router
router = APIRouter(
    prefix="/contacts",
    tags=["contact"],
    responses={404: {"description": "Not Found"}},
)

"""
    A generic CRUD router can be created. 
    Specifically for employee, client, contact , department endpoints as they use only CRUD functionality
"""


def not_found_exception(id):
    """
    Not founds with specific ID exception
    """

    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Contact with id= {id} not found"
    )


@router.get("/", response_model=List[schemas.ContactOut])
def get_all_contacts(db: Session = Depends(get_db)):
    """
    Get all contacts as LIST
    """

    all_contact = contactService.get_multiple(db=db)
    return all_contact


@router.get("/{id}", response_model=schemas.ContactOut)
def get_contact(id: int, db: Session = Depends(get_db), ):
    """
    Get a contact by its ID
    """

    db_contact = contactService.get(db=db, id=id)
    if not db_contact:
        raise not_found_exception(id)

    return db_contact


@router.post("/", response_model=schemas.ContactOut, status_code=status.HTTP_201_CREATED)
def create_contact(contact: schemas.ContactBase, db: Session = Depends(get_db), ):
    """
    Create a contact
    """
    try:
        db_contact = contactService.create(db=db, obj_in=contact)
    except (exc.IntegrityError) as e:
        print(e.orig)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid input")

    return db_contact


@router.put("/{id}", response_model=schemas.ContactOut)
def update_contact(*,
                   id: int,
                   db: Session = Depends(get_db),
                   contact_update: schemas.ContactBase,
                   ) -> Any:
    """
    Update a specific contact
    """

    db_contact = contactService.get(db=db, id=id)
    if not db_contact:
        raise not_found_exception(id)

    try:
        db_contact_updated = contactService.update(db=db, obj_in=contact_update, id=id)
    except (exc.IntegrityError) as e:
        print(e.orig)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid input")

    return db_contact_updated


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_contact(*, db: Session = Depends(get_db), id: int, ):
    """
    Delete a specific contact
    """

    db_contact = contactService.get(db=db, id=id)
    if not db_contact:
        raise not_found_exception(id)

    contactService.delete(db=db, id=id).cascade()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
