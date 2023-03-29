from app.services.defaultService import DefaultService
from app import models, schemas


class DepartmentService(
	DefaultService[models.Department, schemas.DepartmentBase, schemas.DepartmentBase],
):
	"""
	Department service implementing Default_service and its CRUD methods
	"""
	def method_for_sanity_check(self):
		return "returning from child service"


departmentService = DepartmentService(models.Department)
