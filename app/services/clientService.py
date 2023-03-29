from app.services.defaultService import DefaultService
from sqlalchemy.orm import Session
from app import models, schemas
from typing import Any


class ClientService(
	DefaultService[models.Client, schemas.ClientBase, schemas.ClientOut],
):
	"""
	Client service implementing Default_service and its CRUD methods
	"""
	def method_for_sanity_check(self):
		return "returning client from child service"

	def get_contacts_for_client(self, db: Session, client_id: Any):
		return db.query(models.Contact).filter(models.Contact.client_id == client_id).all()

	def get_employees_for_client(self, db: Session, client_id: Any):
			return db.query(models.Employee).filter(models.Employee.client_id == client_id).all()

	def get_departments_for_client(self, db: Session, client_id: Any):
			return db.query(models.Department).filter(models.Department.client_id == client_id).all()


clientService = ClientService(models.Client)
