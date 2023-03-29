*** Settings ***
Documentation		 API Testing in Robot Framework

Library			SeleniumLibrary
Library			RequestsLibrary
Library			JSONLibrary
Library			Collections
Library			OperatingSystem
Library			BuiltIn
Suite Setup		Create new session


*** Variables ***
# ${baseUrl}	https://logichainge-backend-github-26ar3gp3ja-ez.a.run.app.com
${baseUrl}	http://localhost
${Verify}	true
${Session}




*** Test Cases ***
Check for avalability on "/"
	[Documentation]	This test case verifies that the response code of the GET Request should be 200
	[Tags]	smoke
	${response}=	GET On Session	${Session}	/	expected_status=200

Try to upload jsons
	${json}=	Get File	test/robot/json/1.json
	${response}=	POST On Session	${Session}	/json/	data=${json}	expected_status=201
	${json}=	Get File	test/robot/json/2.json
	${response}=	POST On Session	${Session}	/json/	data=${json}	expected_status=201

Check transport files have been added
	${response}=	GET On Session	${Session}	/transport_files/	expected_status=200
	${content}=	Set Variable	${response.json()}

	${content_length}=	Get Length	${content}
	Should Be Equal As Integers	${content_length}	2

Check the files were given default pending state
	${response}=	GET On Session	${Session}	/transport_files/get_by_status/pending	expected_status=200
	${content}=	Set Variable	${response.json()}

	${content_length}=	Get Length	${content}
	Should Be Equal As Integers	${content_length}	2

Check that clients have been crreated
	${response}=	GET On Session	${Session}	/clients	expected_status=200
	${content}=	Set Variable	${response.json()}
	${content_length}=	Get Length	${content}
	Should Be Equal As Integers	${content_length}	2

Check clients information
	${response}=	GET On Session	${Session}	/clients/1	expected_status=200
	${content}=	Set Variable	${response.json()}
	${id}=	Get Value From Json	${content}	$.id
	Should Be Equal As Integers	${id[0]}	1
	${client_identifier}=	Get Value From Json	${content}	$.client_identifier
	Should Be Equal As Strings	${client_identifier[0]}	2
	${response}=	GET On Session	${Session}	/clients/2	expected_status=200
	${content}=	Set Variable	${response.json()}
	${id}=	Get Value From Json	${content}	$.id
	Should Be Equal As Integers	${id[0]}	2
	${client_identifier}=	Get Value From Json	${content}	$.client_identifier
	Should Be Equal As Strings	${client_identifier[0]}	123

Try to update client
	${response}=	GET On Session	${Session}	/clients/1	expected_status=200
	${content}=	Set Variable	${response.json()}
	${content}=	Update Value To Json	${content}	$.client_identifier	test2
	@{name}=	Create list	client1	altNameClient1
	${content}=	Update Value To Json	${content}	$.name	${name}
	${response}=	PUT On Session	${Session}	/clients/1	json=${content}	expected_status=200
	${content}=	Set Variable	${response.json()}
	${client_identifier_new}=	Get Value From Json	${content}	$.client_identifier
	Should Be Equal As Strings	${client_identifier_new[0]}	test2
	${client_name_new}=	Get Value From Json	${content}	$.name
	Should Be Equal As Strings	${client_name_new[0][0]}	client1
	Should Be Equal As Strings	${client_name_new[0][1]}	altNameClient1

Check contacts information
	${response}=	GET On Session	${Session}	/contacts/1	expected_status=200
	${content}=	Set Variable	${response.json()}
	${id}=	Get Value From Json	${content}	$.id
	Should Be Equal As Integers	${id[0]}	1
	${client_id}=	Get Value From Json	${content}	$.client_id
	Should Be Equal As Strings	${client_id[0]}	1

Try to update contact
	${response}=	GET On Session	${Session}	/contacts/1	expected_status=200
	${content}=	Set Variable	${response.json()}
	${initials}=	Get Value From Json	${content}	$.initials
	Should Be Equal As Strings	${initials[0]}	R. T. 2
	${content}=	Update Value To Json	${content}	$.initials	X.Y.
	@{phone}=	Create list	+40-712-3345678	+31-012-2345672
	${content}=	Update Value To Json	${content}	$.phone	${phone}
	${response}=	PUT On Session	${Session}	/contacts/1	json=${content}	expected_status=200
	${content}=	Set Variable	${response.json()}
	${initials_new}=	Get Value From Json	${content}	$.initials
	Should Be Equal As Strings	${initials_new[0]}	X.Y.
	${phone_new}=	Get Value From Json	${content}	$.phone
	Should Be Equal As Strings	${phone_new[0][0]}	+40-712-3345678
	Should Be Equal As Strings	${phone_new[0][1]}	+31-012-2345672

Check departments information
	${response}=	GET On Session	${Session}	/departments/1	expected_status=200
	${content}=	Set Variable	${response.json()}
	${id}=	Get Value From Json	${content}	$.id
	Should Be Equal As Integers	${id[0]}	1
	${client_id}=	Get Value From Json	${content}	$.client_id
	Should Be Equal As Strings	${client_id[0]}	1
	${response}=	GET On Session	${Session}	/departments/2	expected_status=200
	${content}=	Set Variable	${response.json()}
	${id}=	Get Value From Json	${content}	$.id
	Should Be Equal As Integers	${id[0]}	2
	${client_id}=	Get Value From Json	${content}	$.client_id
	Should Be Equal As Strings	${client_id[0]}	2

Try to update department
	${response}=	GET On Session	${Session}	/departments/1	expected_status=200
	${content}=	Set Variable	${response.json()}
	${content}=	Update Value To Json	${content}	$.name	test123
	${response}=	PUT On Session	${Session}	/departments/1	json=${content}	expected_status=200
	${content}=	Set Variable	${response.json()}
	${client_id_new}=	Get Value From Json	${content}	$.client_id
	Should Be Equal As Strings	${client_id_new[0]}	1
	${name_new}=	Get Value From Json	${content}	$.name
	Should Be Equal As Strings	${name_new[0]}	test123

Check employees information
	${response}=	GET On Session	${Session}	/employees/1	expected_status=200
	${content}=	Set Variable	${response.json()}
	${id}=	Get Value From Json	${content}	$.id
	Should Be Equal As Integers	${id[0]}	1
	${client_id}=	Get Value From Json	${content}	$.client_id
	Should Be Equal As Strings	${client_id[0]}	1
	${response}=	GET On Session	${Session}	/employees/2	expected_status=200
	${content}=	Set Variable	${response.json()}
	${id}=	Get Value From Json	${content}	$.id
	Should Be Equal As Integers	${id[0]}	2
	${client_id}=	Get Value From Json	${content}	$.client_id
	Should Be Equal As Strings	${client_id[0]}	2

Try to update employee
	${response}=	GET On Session	${Session}	/employees/1	expected_status=200
	${content}=	Set Variable	${response.json()}
	${content}=	Update Value To Json	${content}	$.name	test123
	${response}=	PUT On Session	${Session}	/employees/1	json=${content}	expected_status=200
	${content}=	Set Variable	${response.json()}
	${client_id_new}=	Get Value From Json	${content}	$.client_id
	Should Be Equal As Strings	${client_id_new[0]}	1
	${name_new}=	Get Value From Json	${content}	$.name
	Should Be Equal As Strings	${name_new[0]}	test123

Check data for the first transport file
	${response}=	GET On Session	${Session}	/transport_files/1	expected_status=200
	${content}=	Set Variable	${response.json()}

	${id}=	Get Value From Json	${content}	$.id
	Should Be Equal As Integers	${id[0]}	1

	${client_id}=	Get Value From Json	${content}	$.client_id
	Should Be Equal As Integers	${client_id[0]}	1

Try to update transport_file
	${response}=	GET On Session	${Session}	/transport_files/1	expected_status=200
	${content}=	Set Variable	${response.json()}
	${content}=	Update Value To Json	${content}	$.display_number	123456
	${content}=	Update Value To Json	${content}	$.urgency	${False}
	${response}=	PUT On Session	${Session}	/transport_files/1	json=${content}	expected_status=200
	${content}=	Set Variable	${response.json()}
	${display_number_new}=	Get Value From Json	${content}	$.display_number
	Should Be Equal As Strings	${display_number_new[0]}	123456
	${urgency_new}=	Get Value From Json	${content}	$.urgency
	Should Be Equal As Strings	${urgency_new[0]}	${False}

Check activities for the first transport file
	${response}=	GET On Session	${Session}	/transport_files/1/activities	expected_status=200
	${content}=	Set Variable	${response.json()}
	${content_length}=	Get Length	${content}
	Should Be Equal As Integers	${content_length}	4
	Should Be Equal As Integers	${content[0]["transport_file_id"]}	1
	${first_activity}=	Set Variable	${content[0]}
	${id}=	Get Value From Json	${first_activity}	$.id
	Should Be Equal As Integers	${id[0]}	1

	${contact_id}=	Get Value From Json	${first_activity}	$.contact_id
	Should Be Equal As Integers	${contact_id[0]}	2

Try to update activity 1 of the first transport file
	${response}=	GET On Session	${Session}	/transport_files/1/activities	expected_status=200
	${content}=		Set Variable	${response.json()}
	${activity}=	Set Variable
	${response}=	GET On Session	${Session}	/transport_files/1	expected_status=200
	${content}=		Set Variable	${response.json()}
	${content}=		Update Value To Json	${content}	$.display_number	123456
	${content}=		Update Value To Json	${content}	$.urgency	${False}
	${response}=	PUT On Session	${Session}	/transport_files/1	json=${content}	expected_status=200
	${content}=		Set Variable	${response.json()}
	${display_number_new}=	Get Value From Json	${content}	$.display_number
	Should Be Equal As Strings	${display_number_new[0]}	123456
	${urgency_new}=	Get Value From Json	${content}	$.urgency
	Should Be Equal As Strings	${urgency_new[0]}	${False}

*** Keywords ***
Create new session
	Create Session	${Session}	${baseUrl}	verify=${Verify}