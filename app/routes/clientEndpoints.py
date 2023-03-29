from fastapi import Depends, APIRouter, Response, status, HTTPException
from sqlalchemy import exc
from sqlalchemy.orm import Session
from app.database.database import get_db
from typing import List, Any
from app import schemas
from app.services.clientService import clientService

# Defining the router
router = APIRouter(
    prefix="/clients",
    tags=["client"],
    responses={404: {"description": "Not Found"}},
)

"""
    A generic CRUD router can be created. 
    Specifically for employee, client, contact , department endpoints as they use only CRUD functionality
"""


def not_found_exception(id):
    """
    No client found with specific ID exception
    """
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Client with id= {id} not found"
    )
    
def entities_not_found_for_client_exception(id, entity_name):
    """
    No entities found for client with specific ID exception
    """
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No {entity_name}s found for client with id= {id} "
    )


@router.get("/", response_model=List[schemas.ClientOut])
def get_all_clients(db: Session = Depends(get_db)):
    """
    Get all clients as LIST
    """

    result = clientService.get_multiple(db=db)
    if not result:
        raise not_found_exception(id)
    return result



@router.get("/{id}", response_model=schemas.ClientOut)
def get_client(id: int, db: Session = Depends(get_db), ):
    """
    Get a client by its ID
    """

    result = clientService.get(db=db, id=id) 
    if not result:
        raise not_found_exception(id)

    return result

@router.get("/{id}/contacts", response_model=List[schemas.ContactOut])
def get_contacts_for_client(id: int, db: Session = Depends(get_db), ):
    """
    Get a list of contacts belonging to a client
    """

    db_client = clientService.get_contacts_for_client(db=db, client_id=id)
    if not db_client:
        raise entities_not_found_for_client_exception(id, "contact")

    return db_client

@router.get("/{id}/employees", response_model=List[schemas.ContactOut])
def get_employees_for_client(id: int, db: Session = Depends(get_db), ):
    """
    Get a list of employees belonging to a client
    """

    db_client = clientService.get_employees_for_client(db=db, client_id=id)
    if not db_client:
        raise entities_not_found_for_client_exception(id, "employee")

    return db_client

@router.get("/{id}/departments", response_model=List[schemas.ContactOut])
def get_departments_for_client(id: int, db: Session = Depends(get_db), ):
    """
    Get a list of departments belonging to a client
    """

    db_client = clientService.get_departments_for_client(db=db, client_id=id)
    if not db_client:
        raise entities_not_found_for_client_exception(id, "department")

    return db_client


@router.post("/", response_model=schemas.ClientOut, status_code=status.HTTP_201_CREATED)
def create_client(client: schemas.ClientBase, db: Session = Depends(get_db), ):
    """
    Create a client
    """
    try:
        db_client = clientService.create(db=db, obj_in=client)
    except (exc.IntegrityError) as e:
        print(e.orig)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid input")

    return db_client


@router.put("/{id}", response_model=schemas.ClientOut)
def update_client(*,
                  id: int,
                  db: Session = Depends(get_db),
                  client_update: schemas.ClientBase,
                  ) -> Any:

    """
    Update a specific client
    """

    db_client = clientService.get(db=db, id=id)
    if not db_client:
        raise not_found_exception(id)

    try:
        db_client_updated = clientService.update(db=db, obj_in=client_update, id=id)
    except (exc.IntegrityError) as e:
        print(e.orig)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid input")

    return db_client_updated


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_client(*, db: Session = Depends(get_db), id: int, ):
    """
    Delete a specific client
    """

    db_client = clientService.get(db=db, id=id)
    if not db_client:
        raise not_found_exception(id)

    clientService.delete(db=db, id=id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
