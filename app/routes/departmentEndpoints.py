from fastapi import Depends, APIRouter, Response, status, HTTPException
from sqlalchemy import exc
from sqlalchemy.orm import Session
from app.database.database import get_db
from typing import List, Any
from app import schemas
from app.services.departmentService import departmentService

# Defining the router
router = APIRouter(
    prefix="/departments",
    tags=["department"],
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
        detail=f"Department with id= {id} not found"
    )


@router.get("/", response_model=List[schemas.DepartmentOut])
def get_all_departments(db: Session = Depends(get_db)):
    """
    Get all departments as LIST
    """

    all_department = departmentService.get_multiple(db=db)
    return all_department


@router.get("/{id}", response_model=schemas.DepartmentOut)
def get_department(id: int, db: Session = Depends(get_db), ):
    """
    Get a department by its ID
    """

    db_department = departmentService.get(db=db, id=id)
    if not db_department:
        raise not_found_exception(id)

    return db_department


@router.post("/", response_model=schemas.DepartmentOut, status_code=status.HTTP_201_CREATED)
def create_department(department: schemas.DepartmentBase, db: Session = Depends(get_db), ):
    """
    Create a department
    """

    try:
        db_department = departmentService.create(db=db, obj_in=department)
    except (exc.IntegrityError) as e:
        print(e.orig)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid input")

    return db_department


@router.put("/{id}", response_model=schemas.DepartmentOut)
def update_department(*,
                      id: int,
                      db: Session = Depends(get_db),
                      department_update: schemas.DepartmentBase,
                      ) -> Any:
    """
    Update a specific department
    """

    db_department = departmentService.get(db=db, id=id)
    if not db_department:
        raise not_found_exception(id)

    try:
        db_department_updated = departmentService.update(db=db, obj_in=department_update, id=id)
    except (exc.IntegrityError) as e:
        print(e.orig)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid input")


    return db_department_updated


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_department(*, db: Session = Depends(get_db), id: int, ):
    """
    Delete a specific department
    """

    db_department = departmentService.get(db=db, id=id)
    if not db_department:
        raise not_found_exception(id)

    departmentService.delete(db=db, id=id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
