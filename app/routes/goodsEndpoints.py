from fastapi import Depends, APIRouter, encoders, Response, HTTPException, status
from sqlalchemy.orm import Session
from app.database.database import get_db
from typing import List
from app import schemas, services, models
from app.services import goodsService
from sqlalchemy import exc

# Defining the router
router = APIRouter(
    prefix="/goods",
    tags=["goods"],
    responses={404: {"description": "Not Found"}},
)


def not_found_exception(id):
    """
    Not founds with specific ID exception
    """

    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Goods item with id= {id} not found"
    )


@router.get("/", response_model=List[schemas.GoodsOut])
def get_all_goods(db: Session = Depends(get_db)):
    """
    Get all goods objects as LIST
    """

    all_files = goodsService.get_all_goods(db)
    return all_files


@router.get("/{id}", response_model=schemas.GoodsOut)
def get_goods(id: int, db: Session = Depends(get_db), ):
    """
    Get a goods object by its ID
    """

    db_goods = goodsService.get_goods(db, id)
    if not db_goods:
        raise not_found_exception(id)
    return db_goods


@router.post("/", response_model=schemas.GoodsOut, status_code=status.HTTP_201_CREATED)
def create_goods(goods: schemas.GoodsBase, db: Session = Depends(get_db), ):
    """
    Create a goods object
    """

    try:
        db_goods = goodsService.save_goods(db, goods)
    except (exc.IntegrityError) as e:
        print(e.orig)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid input")

    return db_goods


@router.put("/{id}", response_model=schemas.GoodsOut)
def update_goods(*,
                 id: int,
                 db: Session = Depends(get_db),
                 goods_update: schemas.GoodsBase,
                 ):
    """
    Update a specific goods object
    """

    db_goods = goodsService.get_goods(db, id)
    if not db_goods:
        raise not_found_exception(id)

    try:
        db_goods_updated = goodsService.update_goods(db, goods_update, id)
    except (exc.IntegrityError) as e:
        print(e.orig)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid input")

    return db_goods_updated


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_goods(*, db: Session = Depends(get_db), id: int, ):
    """
    Delete a specific goods object
    """

    db_goods = goodsService.get_goods(db, id)
    if not db_goods:
        raise not_found_exception(id)

    goodsService.delete_goods(db, id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
