# -*- coding: utf-8 -*-

import json

from uuid import uuid4

import aiohttp
from aiohttp import web

from pathshare_api.models import Ride, User
from pathshare_api.utilities import encrypt_password


class PostEndpoints(object):
    """Encapsulates routes for all POST requests made to the API.
    
    Attributes
    ----------
    db : MongoConnection
        An instance of MongoConnection.
    
    Notes
    -----
    Sample request to /post/user/new using HTTPie:
    `http --form POST :5002/post/user/new name=simon major=cs \
    age=21 username=swoldemi email=swoldemi@gmail.com password=hi`
    
    See Also
    ---------
    https://motor.readthedocs.io/en/stable/api-tornado/motor_collection.html?highlight=aggregate#motor.motor_tornado.MotorCollection.aggregate
    """

    def __init__(self, db):
        self.db = db
    

    async def post_new_user(self, request: aiohttp.web_request.Request) -> web.json_response:
        """Add a new user to the system.
        
        Parameters
        -----------
        aiohttp.web_request.Request
            A request to the endpoint made by the frontend web client.

        Returns
        --------
        web.json_response
        Three types of JSON responses.
            The first occurs when a key is missing. (Status 422 => Unprocessable Entity)
            The second occurs when the email is not unique. (Status 417 => Expectation Failed)
            The third occurs when the new user POST request was successful. (Status 200 => OK)
        
        Notes
        -----
        Expected request format:
        {
            name : string
            major : string
            age : int
            username : string
            email : string
            password : string
        }
        """
        # Wait for a new concurrent POST request to be made
        data = await request.post()

        # Define what data should be in the request
        expceted_keys = ["name", "major", "age", "username", "email", "password"]
        for key in expceted_keys:
            try:
                # Assert that the request contains all expected keys
                assert key in data
            except AssertionError as e:
                return web.json_response({"error": f"Request must contain key: '{key}'."}, status=422)
        
        # Check for duplicates using custom method
        seen = await self.db.is_duplicate_email(data.get("email"))
        if seen:
            return web.json_response({"error": f"Email {data.get('email')} already has associated account."}, status=417)
        
        # Checks have passed, create the user
        user_schema = User()
        password = await encrypt_password(data.get("password"))
        document = dict(
            name=data.get("name"),
            major=data.get("major"),
            age=data.get("age"),
            token=uuid4().hex,
            is_validates=False,
            username=data.get("username"),
            email=data.get("email"),
            password=password,
        )
        document = user_schema.dump(document).data

        # Insert the new user into the database
        await self.db.client.users.insert_one(document)
        return web.json_response({"success": f"Account successfully created."}, status=200)
      

    async def post_new_ride(self, request: aiohttp.web_request.Request):
        """Add a new ride to the system."""
        raise NotImplementedError