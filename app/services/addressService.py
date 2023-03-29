from app.services.defaultService import DefaultService
from app import models, schemas


class AddressService(
	DefaultService[models.Address, schemas.AddressBase, schemas.AddressBase],
):
	"""
	Address service implementing Default_service and its CRUD methods
	"""
	def method_for_sanity_check(self):
		return "returning from child service"


addressService = AddressService(models.Address)
