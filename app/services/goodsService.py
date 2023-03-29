from typing import List, Any
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app import models
from app.schemas.goods import GoodsBase, GoodsOut


def get_all_goods(db: Session):
	"""
	Get all goods items from the db.
	"""
	return db.query(models.Goods).all()


def get_goods(db: Session, id: int):
	"""
	Get a goods item by ID from the db.
	"""
	return db.query(models.Goods).filter(models.Goods.id == id).first()

def get_goods_for_activity(db: Session, activity_id: int):
	"""
	Get a goods item by ID from the db.
	"""
	return db.query(models.Goods).filter(models.Goods.activity_id == activity_id).all()


def save_goods(
		db: Session,
		goods_in: GoodsBase
) -> Any:
	"""
	Save a goods item to the db.
	"""
	goods_data = jsonable_encoder(goods_in)
	db_goods = models.Goods(**goods_data)
	
	db.add(db_goods)
	db.commit()
	db.refresh(db_goods)
	
	return db_goods
	

def save_goods_basic_fields(
		db: Session,
		goods_in: GoodsBase
) -> Any:
	"""
	Save a goods item to the db, but excluding some fields.
	"""
	goods_data = jsonable_encoder(goods_in, exclude={"id"})
	db_goods = models.Goods(**goods_data)
	
	db.add(db_goods)
	db.commit()
	db.refresh(db_goods)
	
	return db_goods


def update_goods(db: Session, goods_update: GoodsBase, id: int):
	"""
	Update a goods item from the db.
	"""
	goods_query = db.query(models.Goods).filter(models.Goods.id == id)
	
	goods_query.update(goods_update.dict())
	db.commit()
	
	return goods_query.first()


def update_goods_basic_fields(db: Session, goods_update: GoodsBase, id: int):
	"""
	Update a goods item from the db, but excluding some fields.
	"""
	
	goods_query = db.query(models.Goods).filter(models.Goods.id == id)
	
	goods_query.update(goods_update.dict(exclude={"id"}))
	db.commit()
	
	return goods_query.first()


def delete_goods(db: Session, id: int):
	"""
	Delete a goods item from the db.
	"""
	goods_to_delete = get_goods(db, id)
	db.delete(goods_to_delete)
	db.commit()
	return goods_to_delete




