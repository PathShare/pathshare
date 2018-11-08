# -*- coding: utf-8 -*-

"""Test suite for api endpoints."""

import asyncio

from json import dumps

import pytest

from pathshare_api.main import init_app


async def test_new_user(aiohttp_client, loop):
	"""Test all return cases of PostEndpoints.post_new_user.
	
	See Also
	--------
	https://docs.aiohttp.org/en/stable/web_reference.html#response-classes
	"""

	# Create an instance of the application
	app = await init_app()

	# Create a new, injected aiohttp_client fixture using the app
	client = await aiohttp_client(app)

	# Define the data used for the application
	data = {
		"name": "simon",
		"major": "Computer Science",
		"age": 21,
		"username": "swoldemi",
		"email": "simon.woldemichael@ttu.edu",
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
	assert result["success"] == "Account successfully created."
