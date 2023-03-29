from fastapi import Depends, APIRouter, Response, status, HTTPException
from sqlalchemy import exc
from sqlalchemy.orm import Session
from app.database.database import get_db
from typing import List, Any
from app import schemas
from app.services.employeeService import employeeService

# Defining router
router = APIRouter(
    prefix="/employees",
    tags=["employee"],
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
        detail=f"Employee with id= {id} not found"
    )
    

@router.get("/", response_model=List[schemas.EmployeeOut])
def get_all_employees(db: Session = Depends(get_db)):
    """
    Get all employees as LIST
    """

    all_employee = employeeService.get_multiple(db=db)
    return all_employee


@router.get("/{id}", response_model=schemas.EmployeeOut)
def get_employee(id: int, db: Session = Depends(get_db), ):
    """
    Get a employee by its ID
    """

    db_employee = employeeService.get(db=db, id=id)
    if not db_employee:
        raise not_found_exception(id)

    return db_employee


@router.post("/", response_model=schemas.EmployeeOut, status_code=status.HTTP_201_CREATED)
def create_employee(employee: schemas.EmployeeBase, db: Session = Depends(get_db), ):
    """
    Create employee
    """
    try:
        db_employee = employeeService.create(db=db, obj_in=employee)
    except (exc.IntegrityError) as e:
        print(e.orig)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid input")

    return db_employee


@router.put("/{id}", response_model=schemas.EmployeeOut)
def update_employee(*,
                    id: int,
                    db: Session = Depends(get_db),
                    employee_update: schemas.EmployeeBase,
                    ) -> Any:
    """
    Update a specific employee
    """

    db_employee = employeeService.get(db=db, id=id)
    if not db_employee:
        raise not_found_exception(id)

    db_employee_updated = employeeService.update(db=db, obj_in=employee_update, id=id)

    return db_employee_updated


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(*, db: Session = Depends(get_db), id: int, ):
    """
    Delete a specific employee
    """

    db_employee = employeeService.get(db=db, id=id)
    if not db_employee:
        raise not_found_exception(id)

    employeeService.delete(db=db, id=id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
