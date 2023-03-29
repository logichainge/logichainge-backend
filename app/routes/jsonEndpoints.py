from fastapi import Depends, APIRouter, encoders, Response, HTTPException, status
from sqlalchemy.orm import Session
from app.database.database import get_db
from typing import List, Any
from app import schemas, models
from app.services import jsonService
from sqlalchemy import exc
import json

# Defining the router
router = APIRouter(
    prefix="/json",
    tags=["json"],
    responses={404: {"description": "Not Found"}},
)


def not_found_exception(id):
    """
    Not founds with specific ID exception
    """

    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Activity with id= {id} not found"
    )

@router.post("/")
def create_json(json_data: schemas.JsonBase , db: Session = Depends(get_db), ):
    """
    populate database with info from json
    """
    json = jsonService.populate_with_data_from_json(db=db, json_data=json_data)
    # try:
    #     jsonService.populate_with_data_from_json(db = db)
    # except (exc.IntegrityError) as e:
    #     print(e.orig)
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid input")

    return Response(status_code=status.HTTP_201_CREATED)