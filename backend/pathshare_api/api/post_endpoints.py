# -*- coding: utf-8 -*-

import json
import os

from datetime import datetime
from uuid import uuid4

import aiohttp

from aiohttp import web
from bson.objectid import ObjectId
from dateutil.parser import parse as parse_date

from pathshare_api.models import Ride, User
from pathshare_api.utilities import encrypt_password, send_email


class PostEndpoints(object):
    """Encapsulates routes for all POST requests made to the API.
    
    Attributes
    ----------
    db : MongoConnection
        An instance of MongoConnection.
    
    Notes
    -----
    content-type header key must always have value `application/json`

    Sample request (raw JSON w/ content-type of application/json) to /post/user/new using Postman:
    (If this test data returns a 422 response, check the database; there is a chance there is already
    an account with the same email.)
    {
        "name": "simon",
        "major": "Computer Science",
        "age": 21,
        "username": "swoldemi",
        "email": "simon.woldemichael@ttu.edu",
        "password": "hello"
    }

    Sample request (raw JSON w/ content-type of application/json) to /post/ride/new using Postman:
    (Set the ObjectIds in the riders array to some user's ObjectId in the database.)
    {
        "riders": [
            "5be52a64dfd3e35fac9fc298"
        ],
        "departure_date": "Dec 2 2018",
        "departure_location": "Lubbock",
        "destination": "Houston",
        "price_per_seat": 5.00
    }

    See Also
    ---------
    https://motor.readthedocs.io/en/stable/api-tornado/motor_collection.html?highlight=aggregate#motor.motor_tornado.MotorCollection.aggregate
    https://httpie.org/doc#non-string-json-fields
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
        data = await request.json()

        # Define what data should be in the request
        expected_keys = ["name", "major", "age", "username", "email", "password"]
        for key in expected_keys:
            try:
                # Assert that the request contains all expected keys
                assert key in data
            except AssertionError:
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
            is_validated=False,
            username=data.get("username"),
            email=data.get("email"),
            password=password,
        )
        document = user_schema.dump(document).data

        # Insert the new user into the database
        inserted_result = await self.db.client.users.insert_one(document)

        # Send a validation email on a new thread
        link = f"{os.environ.get('DOMAIN')}/get/validation?id={inserted_result.inserted_id}&token={document.get('token')}"
        await send_email(document.get("email"), document.get("name"), link)
        return web.json_response({"success": f"Account successfully created: {inserted_result.inserted_id}."}, status=200)
      

    async def post_new_ride(self, request: aiohttp.web_request.Request) -> web.json_response:
        """Add a new ride to the system.
        
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
            riders : List[ObjectID]
            departure_date : str
            departure_location : str
            destination : str
            price_per_seat : float         
        }
        """
        # Wait for a new concurrent POST request to be made
        # Read JSON body
        data = await request.json() 

        # Define what data should be in the request
        expected_keys = ["riders", "departure_date", "departure_location", "destination", "price_per_seat"]
        for key in expected_keys:
            try:
                # Assert that the request contains all expected keys
                assert key in data
            except AssertionError:
                return web.json_response({"error": f"Request must contain key: '{key}'."}, status=422)

        # Make sure the riders listed are active accounts in the database
        riders = data.get("riders")

        for ride_id in riders:
            try:
                _id = ObjectId(ride_id)
            except Exception as e:
                return web.json_response({"error": f"User ID {ride_id} is not valid. Exception: {e}"}, status=417)
            user = await self.db.client.users.find_one({"_id": _id})
            if user is None:
                return web.json_response({"error": f"User ID {ride_id} is not associated to any account."}, status=417)
        
        # Checks have passed, create the ride
        ride_schema = Ride()
        document = dict(
            riders=riders,
            departure_date=parse_date(data.get("departure_date")),
            price_per_seat=data.get("price_per_seat"),
            departure_location=data.get("departure_location"),
            destination=data.get("destination"),
            is_active=False,
        )
        document = ride_schema.dump(document).data

        # Insert the new ride into the database
        inserted_result = await self.db.client.rides.insert_one(document)
        return web.json_response({"success": f"Ride successfully created: {inserted_result.inserted_id}."}, status=200)
