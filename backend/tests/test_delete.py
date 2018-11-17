# -*- coding: utf-8 -*-

"""Test suite for api endpoints."""

import asyncio

from json import dumps

import pytest

from bson.objectid import ObjectId

from pathshare_api.main import init_app


async def test_delete_user(aiohttp_client, loop):
	"""Test all return cases of DeleteEndpoints.delete_user.
	
	See Also
	--------
	https://docs.aiohttp.org/en/stable/web_reference.html#response-classes
	"""
	# Create an instance of the application
	app, _ = init_app()

	# Create a new, injected aiohttp_client fixture using the app
	client = await aiohttp_client(app)

	# Data for a new user
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

	# Request creation of a user to be deleted
	resp = await client.post("/post/user/new", data=dumps(data), headers=headers)

	# Make sure the user was created
	assert resp.status == 200
	result = await resp.json()
	assert "success" in result.keys()
	assert "Account successfully created" in result["success"] 
	user_id = result["success"].split(": ")[1].strip(".") # Keep the user_id for later

	# Test the delete endpoint
	
	# Forget the 'id' request argument 
	resp = await client.delete("/delete/user")
	assert resp.status == 422
	result = await resp.json()
	assert "error" in result.keys()
	assert result["error"] == f"Please provide a user ID as a request argument (key=id)."

	# Include the 'id' argument but don't give it a value 
	resp = await client.delete("/delete/user?id=")	
	assert resp.status == 417
	result = await resp.json()
	assert "error" in result.keys()
	assert "Exception" in result["error"]
	
	# Send an id for a user that doesn't exist
	bad_id = ObjectId()
	resp = await client.delete(f"/delete/user?id={bad_id}")	
	assert resp.status == 404
	result = await resp.json()
	assert "error" in result.keys()
	assert result["error"] == f"There are no user with ID: {bad_id}."

	# Do a valid deletion
	resp = await client.delete(f"/delete/user?id={user_id}")	
	assert resp.status == 200
	result = await resp.json()
	assert "success" in result.keys()
	assert result["success"] == f"Deleted user with ID: {user_id}."


async def test_delete_ride(aiohttp_client, loop):
	"""Test all return cases of DeleteEndpoints.delete_ride.
	
	See Also
	--------
	https://docs.aiohttp.org/en/stable/web_reference.html#response-classes
	"""
	# Create an instance of the application
	app, _ = init_app()

	# Create a new, injected aiohttp_client fixture using the app
	client = await aiohttp_client(app)

	# Data for a new user
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

	# Request creation of a user to be deleted
	resp = await client.post("/post/user/new", data=dumps(data), headers=headers)

	# Make sure the user was created
	assert resp.status == 200
	result = await resp.json()
	assert "success" in result.keys()
	assert "Account successfully created" in result["success"] 
	user_id = result["success"].split(": ")[1].strip(".") # Keep the user_id for later

	# Data for a new ride
	data = {
		"riders": [user_id],
		"departure_date": "December 25 2018",
		"departure_location": "Lubbock",
		"destination": "Houston",
		"price_per_seat": 50
	}

	# Create a ride to be deleted
	resp = await client.post("/post/ride/new", data=dumps(data), headers=headers)

	# Make sure the ride was created
	assert resp.status == 200
	result = await resp.json()
	assert "success" in result.keys()
	assert "Ride successfully created" in result["success"] 
	ride_id = result["success"].split(": ")[1].strip(".") # Keep the ride_id for later

	# Test the delete endpoint
	
	# Forget the 'id' request argument 
	resp = await client.delete("/delete/ride")
	assert resp.status == 422
	result = await resp.json()
	assert "error" in result.keys()
	assert result["error"] == f"Please provide a ride ID as a request argument (key=id)."

	# Include the 'id' argument but don't give it a value 
	resp = await client.delete("/delete/ride?id=")	
	assert resp.status == 417
	result = await resp.json()
	assert "error" in result.keys()
	assert "Exception" in result["error"]
	
	# Send an id for a ride that doesn't exist
	bad_id = ObjectId()
	resp = await client.delete(f"/delete/ride?id={bad_id}")	
	assert resp.status == 404
	result = await resp.json()
	assert "error" in result.keys()
	assert result["error"] == f"There are no ride with ID: {bad_id}."

	# Do a valid ride deletion
	resp = await client.delete(f"/delete/ride?id={ride_id}")	
	assert resp.status == 200
	result = await resp.json()
	assert "success" in result.keys()
	assert result["success"] == f"Deleted ride with ID: {ride_id}."

	# Do a valid user deletion
	resp = await client.delete(f"/delete/user?id={user_id}")	
	assert resp.status == 200
	result = await resp.json()
	assert "success" in result.keys()
	assert result["success"] == f"Deleted user with ID: {user_id}."