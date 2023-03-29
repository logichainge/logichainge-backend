from app.services.defaultService import DefaultService
from app import models, schemas


class ContactService(
	DefaultService[models.Contact, schemas.ContactBase, schemas.ContactBase],
):
	"""
	Contact service implementing Default_service and its CRUD methods
	"""
	def method_for_sanity_check(self):
		return "returning from child service"


contactService = ContactService(models.Contact)
