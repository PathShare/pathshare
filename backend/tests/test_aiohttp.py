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
