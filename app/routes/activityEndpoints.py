from fastapi import Depends, APIRouter, encoders, Response, HTTPException, status
from sqlalchemy.orm import Session
from app.database.database import get_db
from typing import List
from app import schemas, models
from app.services import activityService, goodsService
from sqlalchemy import exc

# Defining the router
router = APIRouter(
    prefix="/activities",
    tags=["activity"],
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

def no_goods_found_exception(id):
    """
    Not founds with specific ID exception
    """

    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No goods found for activity with id= {id}"
    )


@router.get("/", response_model=List[schemas.ActivityOut])
def get_all_activities(db: Session = Depends(get_db)):
    """
    Get all activities as LIST
    """

    all_files = activityService.get_all_activity(db)
    return all_files


@router.get("/{id}", response_model=schemas.ActivityOut)
def get_activity(id: int, db: Session = Depends(get_db), ):
    """
    Get an activity by its ID
    """

    db_activity = activityService.get_activity(db, id)
    if not db_activity:
        raise not_found_exception(id)
    return db_activity

@router.get("/{id}/goods", response_model=List[schemas.GoodsOut])
def get_activity(id: int, db: Session = Depends(get_db), ):
    """
    Get al the goods for an activity by its ID
    """

    db_activity = goodsService.get_goods_for_activity(db, id)
    if not db_activity:
        raise no_goods_found_exception(id)
    return db_activity


@router.post("/", response_model=schemas.ActivityOut, status_code=status.HTTP_201_CREATED)
def create_activity(activity: schemas.ActivityBase, db: Session = Depends(get_db), ):
    """
    Create an activity
    """

    try:
        db_activity = activityService.save_activity(db, activity)
    except (exc.IntegrityError) as e:
        print(e.orig)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid input")

    return db_activity


@router.put("/{id}", response_model=schemas.ActivityOut)
def update_activity(*,
                    id: int,
                    db: Session = Depends(get_db),
                    activity_update: schemas.ActivityBase,
                    ):
    """
    Update a specific activity
    """

    db_activity = activityService.get_activity(db, id)
    if not db_activity:
        raise not_found_exception(id)

    try:
        db_activity_updated = activityService.update_activity(db, activity_update, id)
    except (exc.IntegrityError) as e:
        print(e.orig)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid input")

    return db_activity_updated


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_activity(*, db: Session = Depends(get_db), id: int, ):
    """
    Delete a specific activity
    """

    db_activity = activityService.get_activity(db, id)
    if not db_activity:
        raise not_found_exception(id)

    activityService.delete_activity(db, id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
