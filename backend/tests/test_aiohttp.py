# -*- coding: utf-8 -*-

"""Test suite for api endpoints."""

import asyncio

from json import dumps

import pytest

from bson.objectid import ObjectId

from pathshare_api.main import init_app


async def test_new_user(aiohttp_client, loop):
	"""Test all return cases of PostEndpoints.post_new_user.
	
	See Also
	--------
	https://docs.aiohttp.org/en/stable/web_reference.html#response-classes
	"""

	# Create an instance of the application and a connection to the database
	app, db = init_app()

	# Create a new, injected aiohttp_client fixture using the app
	client = await aiohttp_client(app)

	# Define the data used for the application
	# Go to https://www.mailinator.com/v3/index.jsp?zone=public&query=testing#/#inboxpane to view the test email
	data = {
		"name": "testing",
		"major": "Computer Science",
		"age": 21,
		"username": "testing",
		"email": "testing@mailinator.com", 
		"password": "hello"
	}

	# Set headers
	headers = {
		"content-type": "application/json",
	}

	# Post to the endpoint, make sure to pass data and headers as keyword arguments
	# Notice that data must be dumped using the json.dumps (dump string) function
	resp = await client.post("/post/user/new", data=dumps(data), headers=headers)

	# Assert everything went as expected
	assert resp.status == 200
	result = await resp.json()
	assert "success" in result.keys()
	assert "Account successfully created" in result["success"] 
	user_id = result["success"].split(": ")[1].strip(".") # Keep the user_id for later

	# Do it again and expect an error since the email is not unique
	resp = await client.post("/post/user/new", data=dumps(data), headers=headers)
	assert resp.status == 417
	result = await resp.json()
	assert "error" in result.keys()
	assert result["error"] == f"Email {data.get('email')} already has associated account."

	# Once more, but forget a key
	data.pop("age")
	resp = await client.post("/post/user/new", data=dumps(data), headers=headers)
	assert resp.status == 422
	result = await resp.json()
	assert "error" in result.keys()
	assert result["error"] == "Request must contain key: 'age'."

	# Remove the test document from the database, ensure pymongo.results.DeleteResult returns ack
	deletion_result = await db.client.users.delete_one({"_id": ObjectId(user_id)})
	assert deletion_result.acknowledged

async def test_get_home(aiohttp_client, loop):
	"""Test if home status is 200
	
	See Also
	--------
	https://docs.aiohttp.org/en/stable/web_reference.html#response-classes
	"""

	# Create an instance of the application and a connection to the database
	app, db = init_app()

	# Create a new, injected aiohttp_client fixture using the app
	client = await aiohttp_client(app)

	# GET request to home endpoint
	resp = await client.get("/")
	
	# Assert everything went as expected
	assert resp.status == 200

async def test_get_ride(aiohttp_client, loop):
	"""Test all return cases of GetEnpoint.get_ride.
	
	See Also
	--------
	https://docs.aiohttp.org/en/stable/web_reference.html#response-classes
	"""

	# Create an instance of the application and a connection to the database
	app, db = init_app()

	# Create a new, injected aiohttp_client fixture using the app
	client = await aiohttp_client(app)

	# Define the data used for the application
	# Go to https://www.mailinator.com/v3/index.jsp?zone=public&query=testing#/#inboxpane to view the test email

	#Test - All data keys are present
	data = {
		"dest": "Houston",
		"date": ""
	}

	# Set headers
	headers = {
		"content-type": "application/json",
	}

	# GET request to the endpoint, make sure to pass data and headers as keyword arguments
	resp = await client.get("/get/ride?id=", data=dumps(data), headers=headers)

	# 200 if destiantion is found in the database
	assert resp.status == 200
	result = await resp.json()

	#Check if destination is included on json response
	assert "data" in result.keys()
	assert "destination" in result["data"].keys()
	assert result["data"]["destination"] == data["dest"]

async def test_get_02_ride(aiohttp_client, loop):
	"""Test all return cases of GetEnpoint.get_ride.
	
	See Also
	--------
	https://docs.aiohttp.org/en/stable/web_reference.html#response-classes
	"""

	# Create an instance of the application and a connection to the database
	app, db = init_app()

	# Create a new, injected aiohttp_client fixture using the app
	client = await aiohttp_client(app)

	# Define the data used for the application
	# Go to https://www.mailinator.com/v3/index.jsp?zone=public&query=testing#/#inboxpane to view the test email

	#Test - All data keys are present
	data = {
		"dest": "mkmefwklmfk",
		"date": ""
	}

	# Set headers
	headers = {
		"content-type": "application/json",
	}

	# GET request to the endpoint, make sure to pass data and headers as keyword arguments
	resp = await client.get("/get/ride?id=", data=dumps(data), headers=headers)

	# 404 destiantion is not found in the database
	assert resp.status == 404
	result = await resp.json()

	assert "error" in result.keys()
	assert f"There are no rides in the database that match destination = {data["dest"]}." in result["error"]


	#Test - Data Key "dest" is missing
	data = {
		"date": ""
	}

	# GET request to the endpoint, make sure to pass data and headers as keyword arguments
	resp = await client.get("/get/ride?id=", data=dumps(data), headers=headers)
	# 417 destination key is missing
	assert resp.status == 417

	#Test - Data Key "date" is missing
	data = {
		"dest": ""
	}

	# GET request to the endpoint, make sure to pass data and headers as keyword arguments
	resp = await client.get("/get/ride?id=", data=dumps(data), headers=headers)
	# 417 date key is missing
	assert resp.status == 417

	#Test - Both data keys are missing, empty get request
	data = {
		"": ""
	}

	# GET request to the endpoint, make sure to pass data and headers as keyword arguments
	resp = await client.get("/get/ride?id=", data=dumps(data), headers=headers)
	# 417 destination and date key are missing
	assert resp.status == 417



async def test_get_user(aiohttp_client, loop):
	"""Test all return cases of GetEnpoint.get_user.
	
	See Also
	--------
	https://docs.aiohttp.org/en/stable/web_reference.html#response-classes
	"""

	# Create an instance of the application and a connection to the database
	app, db = init_app()

	# Create a new, injected aiohttp_client fixture using the app
	client = await aiohttp_client(app)

	#Test - All data keys are present
	data = {
		"id": "5be52a64dfd3e35fac9fc298"
	}

	# Set headers
	headers = {
		"content-type": "application/json",
	}

	# GET request to the endpoint, make sure to pass data and headers as keyword arguments
	resp = await client.get("/get/user?id=", data=dumps(data), headers=headers)
	result = await resp.json()

	assert (resp.status == 200) or (resp.status == 404)
	if 'error' in result.keys():
		assert resp.status == 404
	else:
		assert "data" in result.keys()
		assert resp.status == 200
	
	#Test - All data keys are present
	data = {
		"" : ""
	}

	# Set headers
	headers = {
		"content-type": "application/json",
	}

	# GET request to the endpoint, make sure to pass data and headers as keyword arguments
	resp = await client.get("/get/user?id=", data=dumps(data), headers=headers)
	result = await resp.json()

	assert resp.status == 417
	assert "error" in result.keys()
	assert "Please provide a user ID as a request argument (key=id)." == result["error"]
	

async def test_get_all_rides(aiohttp_client, loop):
	"""Test all return cases of GetEnpoint.get_all_rides.
	
	See Also
	--------
	https://docs.aiohttp.org/en/stable/web_reference.html#response-classes
	"""

	# Create an instance of the application and a connection to the database
	app, db = init_app()

	# Create a new, injected aiohttp_client fixture using the app
	client = await aiohttp_client(app)

	# GET request to the endpoint, make sure to pass data and headers as keyword arguments
	resp = await client.get("/get/ride/all")
	result = await resp.json()

	if "error" in result.keys():
		assert resp.status == 404
		return
	assert resp.status == 200

async def test_get_validation(aiohttp_client, loop):
	"""Test all return cases of GetEnpoint.get_validation.
	
	See Also
	--------
	https://docs.aiohttp.org/en/stable/web_reference.html#response-classes
	"""

	# Create an instance of the application and a connection to the database
	app, db = init_app()

	# Create a new, injected aiohttp_client fixture using the app
	client = await aiohttp_client(app)

	# GET request to the endpoint, make sure to pass data and headers as keyword arguments
	resp = await client.get("/get/validation")
	result = await resp.json()

	### Continue test validation here ############

