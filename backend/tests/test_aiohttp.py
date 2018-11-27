# -*- coding: utf-8 -*-

"""Test suite for api endpoints."""

import asyncio

from json import dumps

import pytest

import datetime

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
		"email": "testing@mailinato40.com", 
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

	date_time = str(datetime.datetime.today())
	# Define the data used for the application
	# Go to https://www.mailinator.com/v3/index.jsp?zone=public&query=testing#/#inboxpane to view the test email

	#Create new User:

	data = {
		"name": "testing",
		"major": "Computer Science",
		"age": 21,
		"username": "testing",
		"email": "testing@mailinat12.com", 
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

	# Create Ride:

	# Data for a new destination
	data_dest = {
            "riders" : [user_id],
            "departure_date" : date_time,
            "departure_location" : ["Lubbock"],
            "destination" : "Houston",
            "price_per_seat" : 15.5       
    }

	# Set headers
	headers = {
		"content-type": "application/json",
	}

	# Request creation of a user to be deleted
	resp = await client.post("/post/ride/new", data=dumps(data_dest), headers=headers)

	# Make sure the user was created
	assert resp.status == 200
	result = await resp.json()
	assert "success" in result.keys()
	assert f"Ride successfully added." in result["success"] 

	#Test - All data keys are present
	
	# GET request to the endpoint, make sure to pass data and headers as keyword arguments
	resp = await client.get("/get/ride?dest=Houston&date=" + date_time)

	# 200 if destiantion is found in the database
	assert resp.status == 200
	result = await resp.json()

	#Check if destination is included on json response
	assert "data" in result.keys()

	# Remove the test document from the database, ensure pymongo.results.DeleteResult returns ack
	deletion_result = await db.client.users.delete_one({"_id": ObjectId(user_id)})
	assert deletion_result.acknowledged

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
	resp = await client.get("/get/ride?dest=mkmefwklmfk&date=", headers=headers)

	# 404 destiantion is not found in the database
	assert resp.status == 404
	result = await resp.json()

	assert "error" in result.keys()
	assert f"There are no rides in the database that match destination = {data['dest']}." in result["error"]


	#Test - Data Key "dest" is missing
	data = {
		"date": ""
	}

	# GET request to the endpoint, make sure to pass data and headers as keyword arguments
	resp = await client.get("/get/ride?date=")
	# 417 destination key is missing
	assert resp.status == 417

	#Test - Data Key "date" is missing
	data = {
		"dest": ""
	}

	# GET request to the endpoint, make sure to pass data and headers as keyword arguments
	resp = await client.get("/get/ride?dest=")
	# 417 date key is missing
	assert resp.status == 417

	#Test - Both data keys are missing, empty get request
	data = {
		"": ""
	}

	# GET request to the endpoint, make sure to pass data and headers as keyword arguments
	resp = await client.get("/get/ride?")
	# 417 destination and date key are missing
	assert resp.status == 417



async def test_get_user(aiohttp_client, loop):
	"""Test all return cases of GetEnpoint.get_user.
	
	See Also
	--------
	https://docs.aiohttp.org/en/stable/web_reference.html#response-classes
	"""
	# Create an instance of the application
	app, db = init_app()

	# Create a new, injected aiohttp_client fixture using the app
	client = await aiohttp_client(app)

	# Data for a new user
	data = {
		"name": "test",
		"major": "Computer Science",
		"age": 21,
		"username": "testing",
		"email": "testing@mailinato3.com", 
		"password": "hello"
	}

	# Set headers
	headers = {
		"content-type": "application/json",
	}

	# Request creation of a user to be deleted
	resp = await client.post("/post/user/new", data=dumps(data), headers=headers)

	# Make sure the user was created
	assert resp.status == 200
	result = await resp.json()
	assert "success" in result.keys()
	assert "Account successfully created" in result["success"] 
	user_id = result["success"].split(": ")[1].strip(".") # Keep the user_id for deletion

	# Test - Id missing

	# GET request to the endpoint, make sure to pass data and headers as keyword arguments
	resp = await client.get("/get/user?")
	result = await resp.json()
	assert resp.status == 417
	assert "error" in result.keys()
	assert result["error"] == f"Please provide a user ID as a request argument (key=id)."

	#Test - Id is empty

	# GET request to the endpoint, make sure to pass data and headers as keyword arguments
	resp = await client.get("/get/user?id=")
	assert resp.status == 500

	#Test - user found

	# GET request to the endpoint, make sure to pass data and headers as keyword arguments
	resp = await client.get(f"/get/user?id={user_id}")
	result = await resp.json()
	assert resp.status == 200
	assert "data" in result.keys()

	# Do a valid deletion
	# Remove the test document from the database, ensure pymongo.results.DeleteResult returns ack
	deletion_result = await db.client.users.delete_one({"_id": ObjectId(user_id)})
	assert deletion_result.acknowledged

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

	assert resp.status == 200

async def test_get_validation(aiohttp_client, loop):
	"""Test all return cases of GetEnpoint.get_validation.
	
	See Also
	--------
	https://docs.aiohttp.org/en/stable/web_reference.html#response-classes
	"""

	# # Data for a new user
	# data = {
	# 	"name": "test",
	# 	"major": "Computer Science",
	# 	"age": 21,
	# 	"username": "testing",
	# 	"email": "testing@mailinator.com", 
	# 	"password": "hello"
	# }

	# # Set headers
	# headers = {
	# 	"content-type": "application/json",
	# }

	# # Request creation of a user to be deleted
	# resp = await client.post("/post/user/new", data=dumps(data), headers=headers)

	# # Make sure the user was created
	# assert resp.status == 200
	# result = await resp.json()
	# assert "success" in result.keys()
	# assert "Account successfully created" in result["success"] 
	# user_id = result["success"].split(": ")[1].strip(".") # Keep the user_id for later







	# # Create an instance of the application and a connection to the database
	# app, db = init_app()

	# # Create a new, injected aiohttp_client fixture using the app
	# client = await aiohttp_client(app)

	# # GET request to the endpoint, make sure to pass data and headers as keyword arguments
	# resp = await client.get("/get/validation")
	# result = await resp.json()

	# ### Continue test validation here ############

