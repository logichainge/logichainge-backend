from typing import List, Generic, Type, Any
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy import update
from app import models
from app.schemas import ActivityBase, ClientBase, ContactBase, TransportFileBase, GoodsBase, AddressBase, DepartmentBase, EmployeeBase, JsonBase
from sqlalchemy import exc
from pydantic import errors
from app.models import Activity


def get_fields(item):
	fields = {'all':0, 'completed':0}
	for key in item:
		fields["all"] += 1
		if not item[key] == None and not item[key] == [] and not item[key] == [""] and not item[key] == "":
			fields["completed"]+=1
	return fields

def without_keys(d, keys):
	return {k: d[k] for k in d.keys() - keys}
	
def populate_with_data_from_json(
		db: Session,
		json_data: Any
) -> Any:
	"""
	Save new activity item to the db from parent transport_file, but excluding some fields.
	"""
	transport_file = {}
	client = {}
	contact = {}
	department = {}
	employee = {}
	activities = []
	activity = {}
	address = {}
	goods = []
	good = {}
	json = jsonable_encoder(json_data)["json_data"]

	all_fields = 0
	completed_fields = 0
	
	client.update({
		"client_identifier":json["client"]["client_identifier"],\
		"name":json["client"]["name"]
	})

	fields = get_fields(json["client"])
	all_fields += fields["all"]
	completed_fields += fields["completed"]

	db_client = models.Client(**client)
	db.add(db_client)
	db.commit()
	db.refresh(db_client)

	contact.update({
		"client_id":db_client.id,\
		"initials":json["contact"]["initials"],\
		"name":json["contact"]["name"],\
		"surname":json["contact"]["surname"],\
		"surname_prefix":json["contact"]["surname_prefix"],\
		"phone":json["contact"]["phone"],\
		"mobile":json["contact"]["mobile"],\
		"email":json["contact"]["email"]      
	})

	fields = get_fields(without_keys(contact, {"client_id", "initials", "name", "surname", "surname_prefix"}))
	all_fields += fields["all"]
	completed_fields += fields["completed"]

	db_contact = models.Contact(**contact)
	db.add(db_contact)
	db.commit()
	db.refresh(db_contact)
 
	department.update({
		"client_id":db_client.id,\
	})

	if len(json["department"]["name"]) > 0:
		department.update({"name":json["department"]["name"][0]})
	else:
		department.update({"name":""})

	# fields = get_fields(json["department"])
	# all_fields += fields["all"]
	# completed_fields += fields["completed"]
	
	db_department = models.Department(**department)
	db.add(db_department)
	db.commit()
	db.refresh(db_department)
 
	employee.update({
		"client_id":db_client.id,\
	})

	if len(json["employee"]["name"]) > 0:
		employee.update({"name":json["employee"]["name"][0]})
	else:
		employee.update({"name":""})

	# fields = get_fields(json["employee"])
	# all_fields += fields["all"]
	# completed_fields += fields["completed"]

	db_employee = models.Employee(**employee)
	db.add(db_employee)
	db.commit()
	db.refresh(db_employee)
	
	transport_file.update({
		"client_id":db_client.id, \
		"contact_id":db_contact.id, \
		"department_id":db_department.id, \
		"employee_id":db_employee.id, \
		"display_number":json["display_number"], \
		"tr_file_status":json["tr_file_status"], \
		"invoice_reference":json["invoice_reference"], \
		"file_type":json["file_type"], \
		"equipment_type":json["equipment_type"], \
		"modality":json["modality"],\
		"service_level":json["service_level"],\
		"customs":json["customs"], \
		"attention_required":json["attention_required"],\
		"multi_trip":json["multi_trip"], \
		"multi_activity":json["multi_activity"], \
		"date_deviation":json["date_deviation"], \
		"urgency":json["urgency"], \
		"late_booking":json["late_booking"], \
		"cost_code":json["cost_code"], \
		"reference":json["reference"], \
		"document_reference": json["document_reference"]
	})

	transport_file_clean = without_keys(transport_file, {
							"client_id",\
							"contact_id",\
							"department_id",\
							"employee_id",\
							"display_number",\
							"tr_file_status",\
							"file_type",\
							"equipment_type",\
							"modality",\
							"service_level",\
							"customs",\
							"cost_code",\
							"reference"
							})
	fields = get_fields(transport_file_clean)
	all_fields += fields["all"]
	completed_fields += fields["completed"]

	db_transport_file = models.TransportFile(**transport_file)
	db.add(db_transport_file)
	db.commit()
	db.refresh(db_transport_file)

	activities = json["activities"]
	goods = json["goods"]
	for a in activities:
		activity = {}
		contact.update({
			"client_id":None,\
			"initials":a["contact"]["initials"],\
			"name":a["contact"]["name"],\
			"surname":a["contact"]["surname"],\
			"surname_prefix":a["contact"]["surname_prefix"],\
			"phone":a["contact"]["phone"],\
			"mobile":a["contact"]["mobile"],\
			"email":a["contact"]["email"]
		})

		fields = get_fields(without_keys(contact, {"client_id", "initials", "name", "surname", "surname_prefix"}))
		all_fields += fields["all"]
		completed_fields += fields["completed"]

		db_contact = models.Contact(**contact)
		db.add(db_contact)
		db.commit()
		db.refresh(db_contact)


		address.update({
			"name":a["address"]["name"],\
			"street_1":a["address"]["street_1"],\
			"street_2":a["address"]["street_2"],\
			"street_3":a["address"]["street_3"],\
			"zipcode":a["address"]["zipcode"],\
			"city":a["address"]["city"],\
			"country":a["address"]["country"]
		})

		if len(a["address"]["latitude"]) > 0:
			address.update({
				"latitude":a["address"]["latitude"][0],\
			})
		else:
			address.update({
				"latitude":0,\
			})

		if len(a["address"]["longitude"]) > 0:
			address.update({
				"longitude":a["address"]["longitude"][0],\
			})
		else:
			address.update({
				"longitude":0,\
			})

		fields = get_fields(without_keys(address, {"name", "street_2", "street_3", "latitude", "longitude"}))
		all_fields += fields["all"]
		completed_fields += fields["completed"]

		db_address = models.Address(**address)
		db.add(db_address)
		db.commit()
		db.refresh(db_address)

		activity.update({
			"transport_file_id":db_transport_file.id,\
			"address_id":db_address.id,\
			"contact_id":db_contact.id,\
			"sequence_id":a["sequence_id"],\
			"activity_type":a["activity_type"],\
			"date":a["date"],\
			"time_prefix":a["time_prefix"],\
			"time_1":a["time_1"],\
			"time_2":a["time_2"],\
			"activity_reference":a["activity_reference"],\
			"instructions":a["instructions"],\
		})

		activity_clean = without_keys(activity, {"transport_file_id", "contact_id", "address_id", "sequence_id", "activity_type", "time_prefix", "instructions"})
		fields = get_fields(activity_clean)
		all_fields += fields["all"]
		completed_fields += fields["completed"]
		db_activity = models.Activity(**activity)
		db.add(db_activity)
		db.commit()
		db.refresh(db_activity)

		
		for g in goods:
			good = {}
			if g["activity_sequence_id"] == activity["sequence_id"]:
				good.update({
					"activity_id":db_activity.id,\
					"unit_type":g["unit_type"],\
					"stackable":g["stackable"],\
					"quantity":g["quantity"],\
					"description":g["description"],\
					"loading_meters":g["loading_meters"],\
					"net_weight":g["net_weight"],\
					"gross_weight":g["gross_weight"],\
					"dangerous_goods":g["dangerous_goods"],\
					"dg_class":g["dg_class"],\
					"dg_product_group":g["dg_product_group"],\
					"dg_un_code":g["dg_un_code"],\
					"dg_technical_name":g["dg_technical_name"],\
					"size":g["size"],\
					"volume_cbm":g["volume_cbm"]
				})
				if g["measure_unit"] is None:
					good.update({"measure_unit":[]})
				else:
					good.update({"measure_unit":g["measure_unit"]})
				fields = get_fields(without_keys(good, {"activity_id", "dangerous_goods", "dg_class", "dg_product_group", "dg_un_code", "dg_technical_name"}))
				all_fields += fields["all"]
				completed_fields += fields["completed"]
				db_good = models.Goods(**good)
				db.add(db_good)
				db.commit()
				db.refresh(db_good)
	
	if len(activities) == 2:
		first_activity = db.query(models.Activity).filter(models.Activity.transport_file_id == db_transport_file.id).order_by(models.Activity.sequence_id.asc()).first()
		for g in goods:
				good = {}
				if g["activity_sequence_id"] == None:
					good.update({
						"activity_id":first_activity.id,\
						"unit_type":g["unit_type"],\
						"stackable":g["stackable"],\
						"quantity":g["quantity"],\
						"description":g["description"],\
						"loading_meters":g["loading_meters"],\
						"net_weight":g["net_weight"],\
						"gross_weight":g["gross_weight"],\
						"measure_unit":g["measure_unit"],\
						"dangerous_goods":g["dangerous_goods"],\
						"dg_class":g["dg_class"],\
						"dg_product_group":g["dg_product_group"],\
						"dg_un_code":g["dg_un_code"],\
						"dg_technical_name":g["dg_technical_name"],\
						"size":g["size"],\
						"volume_cbm":g["volume_cbm"]
					})
					if g["measure_unit"] is None:
						good.update({"measure_unit":[]})
					else:
						good.update({"measure_unit":g["measure_unit"]})

					fields = get_fields(without_keys(good, { "activity_id", "dangerous_goods", "dg_class", "dg_product_group", "dg_un_code", "dg_technical_name"}))
					all_fields += fields["all"]
					completed_fields += fields["completed"]
					db_good = models.Goods(**good)
					db.add(db_good)
					db.commit()
					db.refresh(db_good)

	certainty = round(completed_fields/all_fields*100, 2)
	stmt = (
		update(models.TransportFile)
		.where(models.TransportFile.id == db_transport_file.id)
		.values({'certainty' : certainty})
	)
	db.execute(stmt)
	db.commit()
	print(certainty)
	return True

