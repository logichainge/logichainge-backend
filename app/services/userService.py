from app.services.defaultService import DefaultService
from sqlalchemy.orm import Session
from app import models, schemas
from typing import Any
from fastapi.security import OAuth2PasswordBearer
from app.database.database import get_db
from passlib.context import CryptContext
from fastapi.encoders import jsonable_encoder



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_all_users(db: Session):
	all_users = db.query(models.User).all()
	return all_users

def method_for_sanity_check(self):
	return "returning client from child service"

def get_hashed_password(password: str) -> str:
	return pwd_context.hash(password)

def get_user_by_username(db : Session, username: str):
	user =  db.query(models.User).filter(models.User.username == username).first()
	return user

def get_user_by_id(db : Session, id: int):
	user =  db.query(models.User).filter(models.User.id == id).first()
	return user

def verify_password(plain_password, hashed_passw):
	return pwd_context.verify(plain_password, hashed_passw)

def authenticate_user(db : Session, username: str, password: str, ):
	user = get_user_by_username(db, username)
	if not user:
		return False
	if not verify_password(password, user.hashed_pass):
		return False
	return user

def create_user(db: Session, user_in: schemas.UserIn):
	user_data = jsonable_encoder(user_in)
	user_data["hashed_pass"] = get_hashed_password(user_data["password"])
	user_data.pop("password")
	if(user_data["is_admin"] is None):
		user_data["is_admin"] = False
	if(user_data["first_login"] is None):
		user_data["first_login"] = True
	if(user_data["password_reset_needed"] is None):
		user_data["password_reset_needed"] = True
	db_user = models.User(**user_data)
	
	db.add(db_user)
	db.commit()
	db.refresh(db_user)
	return db_user

def update_user(db: Session, user_in: schemas.UserIn):
	user_data = jsonable_encoder(user_in)
	user_data["hashed_pass"] = get_hashed_password(user_data["password"])
	user_data.pop("password")
	db_user = models.User(**user_data)
	
	db.add(db_user)
	db.commit()
	db.refresh(db_user)
	return db_user

def reset_password(db: Session, id: int, temporary_password: str):
	user =  db.query(models.User).filter(models.User.id == id).first()
	user.password_reset_needed = True
	user.hashed_pass = get_hashed_password(temporary_password)
	db.add(user)
	db.commit()
	db.refresh(user)
	return user

def change_temp_password(db: Session, id: int, password: str):
	user =  db.query(models.User).filter(models.User.id == id).first()
	user.password_reset_needed = False
	user.first_login = False
	user.hashed_pass = get_hashed_password(password)
	db.add(user)
	db.commit()
	db.refresh(user)
	return user

def delete_user_by_id(db: Session, id: int) -> Any:
	"""
	Delete a user form the db.
	"""
	user_to_delete = get_user_by_id(db, id)
	db.delete(user_to_delete)
	db.commit()
	return user_to_delete


