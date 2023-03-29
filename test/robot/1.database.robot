*** Settings ***
Documentation  Database Testing in Robot Framework
Library  DatabaseLibrary
Library  BuiltIn

*** Variables ***
${DBName}  robot_tests
${DBUser}  logichainge
${DBPassword}  logichainge
${DBHost}  ec2-52-58-30-121.eu-central-1.compute.amazonaws.com
${DBPort}  5432

*** Test Cases ***
Clean Database
	[documentation]  This test case cleans the database of any information and restarts the sequences
	Connect DB
	Log To Console	Connected to DB
	${output}=	Execute SQL String	TRUNCATE employee, department, contact, client, address, goods, activity , transport_file;
	Log To Console	Truncated tables: ${output}
	${output}=	Execute SQL String	ALTER SEQUENCE employee_id_seq RESTART WITH 1;
	${output}=	Execute SQL String	ALTER SEQUENCE department_id_seq RESTART WITH 1;
	${output}=	Execute SQL String	ALTER SEQUENCE contact_id_seq RESTART WITH 1;
	${output}=	Execute SQL String	ALTER SEQUENCE client_id_seq RESTART WITH 1;
	${output}=	Execute SQL String	ALTER SEQUENCE address_id_seq RESTART WITH 1;
	${output}=	Execute SQL String	ALTER SEQUENCE goods_id_seq RESTART WITH 1;
	${output}=	Execute SQL String	ALTER SEQUENCE activity_id_seq RESTART WITH 1;
	${output}=	Execute SQL String	ALTER SEQUENCE transport_file_id_seq RESTART WITH 1;
	Disconnect DB

# Verify Successful creation of Table
#	 [documentation]  This test case verifies that user is able to create a table successfully
#	 Connect DB
#	 ${output}=  Execute SQL String  CREATE TABLE Persons (PersonID int, FirstName varchar(255), Address varchar(255), City varchar(255));
#	 Should Be Equal As Strings  ${output}  None

# Verify Data Insertion in Table
#	 [documentation]  This test case verifies that user is able to insert data in the table successfully
#	 ${output}=  Execute SQL Script  ./Resources/DB Data/insert.sql
#	 Should Be Equal As Strings  ${output}  None

# Verify Data Update in Table
#	 [documentation]  This test case verifies a user can Update a Table record
#	 ${output}=  Execute SQL String  UPDATE Persons SET FirstName = "Kevin" WHERE City="Vantaa";
#	 Should Be Equal As Strings  ${output}  None

# Verify a certain record is present or Not
#	 [documentation]  This test case verifies that in Persons Table we have the data for Dwight
#	 Check If Exists In Database  SELECT PersonID FROM Persons WHERE FirstName="Dwight"

# Verify a Table is present or Not
#	 [documentation]  This test case verifies whether Persons table exist in the database or not
#	 Table Must Exist  Persons

# Verify that the row count is 1
#	 [documentation]  This test case verifies that there is only one row in the table where the city is Espoo
#	 Row Count Is Equal To X  SELECT PersonID FROM Persons WHERE CITY="Espoo"  1

# Verify that you can Delete a Table
#	 [documentation]  This test case verifies that a user can delete a Table
#	 ${output}=  Execute SQL String  DROP TABLE Persons;
#	 Should Be Equal As Strings  ${output}  None
#	 Disconnect DB

*** Keywords ***
Connect DB
	Connect To Database  psycopg2  ${DBName}  ${DBUser}  ${DBPassword}  ${DBHost}  ${DBPort}

Disconnect DB
	Disconnect From Database