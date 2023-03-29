TRUNCATE 
employee,
department,
contact,
client,
address,
goods,
activity ,
transport_file
;
ALTER SEQUENCE employee_id_seq RESTART WITH 1;
ALTER SEQUENCE department_id_seq RESTART WITH 1;
ALTER SEQUENCE contact_id_seq RESTART WITH 1;
ALTER SEQUENCE client_id_seq RESTART WITH 1;
ALTER SEQUENCE goods_id_seq RESTART WITH 1;
ALTER SEQUENCE activity_id_seq RESTART WITH 1;
ALTER SEQUENCE transport_file_id_seq RESTART WITH 1;
ALTER SEQUENCE addressid_seq RESTART WITH 1