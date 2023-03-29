from fastapi import Depends, APIRouter, encoders, Response, HTTPException, status
from sqlalchemy import exc
from sqlalchemy.orm import Session
from app.database.database import get_db
from typing import List
from app import schemas, services, models
from app.services.addressService import addressService

# Defining the router
router = APIRouter(
	prefix="/addresses",
	tags=["address"],
	responses={404: {"description": "Not Found"}},
)

def not_found_exception(id):
	"""
	Not founds with specific ID exception
	"""

	return HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail=f"Address  with id= {id} not found"
		)


@router.get("/", response_model=List[schemas.AddressOut])
def get_all_address(db: Session = Depends(get_db)):
	"""
	Get all addresses as LIST
	"""

	all_files = addressService.get_multiple(db=db)
	return all_files


@router.get("/{id}", response_model=schemas.AddressOut)
def get_address(id: int, db: Session = Depends(get_db), ):
	"""
	Get an address by its ID
	"""

	db_address = addressService.get(db=db, id=id)
	if not db_address:
		raise not_found_exception(id)
	return db_address


@router.post("/", response_model=schemas.AddressOut, status_code=status.HTTP_201_CREATED)
def create_address(address: schemas.AddressBase, db: Session = Depends(get_db), ):
	"""
	Create an address
	"""
	try:
		db_address = addressService.create(db=db, obj_in=address)
	except (exc.IntegrityError) as e:
		print(e.orig)
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid input")

	return db_address


@router.put("/{id}", response_model=schemas.AddressOut)
def update_address(*, id: int, db: Session = Depends(get_db), address_update: schemas.AddressBase, ):
	"""
	Update a specific address
	"""

	db_address = addressService.get(db=db, id=id)
	if not db_address:
		raise not_found_exception(id)

	try:
		db_address_updated = addressService.update(db=db, obj_in=address_update, id=id)
	except (exc.IntegrityError) as e:
		print(e.orig)
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid input")

	return db_address_updated


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_address(*, db: Session = Depends(get_db), id: int, ):
	"""
	Delete a specific address
	"""

	db_address = addressService.get(db=db, id=id)
	if not db_address:
		raise not_found_exception(id)

	addressService.delete(db=db, id=id)
	return Response(status_code=status.HTTP_204_NO_CONTENT)
