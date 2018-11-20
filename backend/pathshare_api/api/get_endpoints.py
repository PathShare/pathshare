# -*- coding: utf-8 -*-

import aiohttp

from aiohttp import web
from bson.objectid import ObjectId

from pathshare_api.utilities import decrypt_password


class GetEndpoints(object):
    """Encapsulates routes for all GET requests made to the API.
    
    Attributes
    ----------
    db : MongoConnection
        An instance of MongoConnection.

    Notes
    -----
    Example get_ride call: localhost:5002/get/ride?dest=Houston
    Example get_user call: localhost:5002/get/user?id=5be52a64dfd3e35fac9fc298
    Example get_all_rides call: localhost:5002/get/ride/all
    Example get_validation: This should not be called directly. Only linked via Email verification.
    """
    def __init__(self, db):
        self.db = db


    async def home(self, request: aiohttp.web_request.Request) -> web.json_response:
        """Default home route for completeness."""
        peername = request.transport.get_extra_info("peername")
        if peername is not None:
            host, port = peername
            return web.json_response({"data": f"Hello from the PathShare API - {host}:{port}."}, status=200)
        return web.json_response({"data": "Hello from the PathShare API."}, status=200)


    async def get_ride(self, request: aiohttp.web_request.Request) -> web.json_response:
        """Get the data of a single ride.
        
        Parameters
        -----------
        aiohttp.web_request.Request
            A request to the endpoint made by the frontend web client.

        Returns
        --------
        aiohttp.web.json_response
        Two types of JSON responses.
            The first occurs when an argument is missing (dest or date). (Status 417 => Expectation Failed)
            The second occurs when a query is successful. (Status 200 => OK)
        """
        dest = request.rel_url.query.get("dest", None)
        if dest is None:
            return web.json_response({"error": "Please provide a destination as a request argument (key=dest)."}, status=417)
        
        """
        date = request.rel_url.query.get("date", None)
        if date is None:
            return web.json_response({"error": "Please provide a date as a request argument (key=date)."}, status=417)
        """
        data = []
        async for ride in self.db.client.rides.find({"destination": dest}):
            ride["_id"] = str(ride.get("_id"))
            data.append(ride)
        if not data:
             return web.json_response({"error": f"There are no rides in the database that match destination = {dest}."}, status=404)
        return web.json_response({"data": data}, status=200)
    

    async def get_user(self, request: aiohttp.web_request.Request) -> web.json_response:
        """Get the data of a single user.
        
        Parameters
        -----------
        aiohttp.web_request.Request
            A request to the endpoint made by the frontend web client.

        Returns
        --------
        aiohttp.web.json_response
        Two types of JSON responses.
            The first occurs when a user does not exist. (Status 417 => Expectation Failed)
            The second occurs when a user ID is valid. (Status 200 => OK)
        """
        email = request.rel_url.query.get("email", None)
        if email is None:
            return web.json_response({"error": "Please provide an email as a request argument (key=email)."}, status=417)

        data = await self.db.client.users.find_one({"email": email})
        if not data:
            return web.json_response({"error": f"There is no user with email: {email}."}, status=404)
        data["_id"] = str(data.pop("_id")) # Hacky 'seralization' of ObjectId
        data["password"] = await decrypt_password(data.pop("password")) # Update password key with decrypted password
        return web.json_response({"data": data}, status=200)


    async def get_all_rides(self, request: aiohttp.web_request.Request) -> web.json_response:
        """Get all of the rides from the rides collection.
        
        Parameters
        -----------
        aiohttp.web_request.Request
            A request to the endpoint made by the frontend web client.

        Returns
        --------
        aiohttp.web.json_response
        Two types of JSON responses.
            The first occurs on an unexpected error. 
                Possibly a timeout if there are far too many rides. (Status 404 => Request Timeout)
            The second occurs when all rides were retrieved successfully. (Status 200 => OK)
        """
        data = []
        async for ride in self.db.client.rides.find():
            ride["_id"] = str(ride.get("_id"))
            data.append(ride)
        if not data:
             return web.json_response({"error": "There are no rides in the database."}, status=404)
        return web.json_response({"data": data}, status=200)


    async def get_validation(self, request: aiohttp.web_request.Request) -> web.json_response:
        """Verify a user based on the URL sent to their inbox on account creation.

        Parameters
        -----------
        aiohttp.web_request.Request
            A request to the endpoint made by the frontend web client.

        Returns
        --------
        aiohttp.web.json_response
        Two types of JSON responses.
            The first occurs when an argument is missing (id or token). (Status 417 => Expectation Failed)
            The second occurs when verification is successful. (Status 200 => OK)
        """
        _id = request.rel_url.query.get("id", None)
        if _id is None:
            return web.json_response({"error": "Please provide a user ID as a request argument. (key=id)"}, status=417)
        
        token = request.rel_url.query.get("token", None)
        if token is None:
            return web.json_response({"error": "Please provide a verification token as a request argument (key=token)."}, status=417)
        
        # Try to find a user with id _id
        user_id = ObjectId(_id)
        data = await self.db.client.users.find_one({"_id": user_id})
        if not data:
            return web.json_response({"error": f"There are no user with ID: {_id}."}, status=417)

        # If the tokens are the same, update the document
        if token == data["token"]:
            await self.db.client.users.find_one_and_update({"_id": user_id}, {"$set": {"is_validated": True}})
            return web.json_response({"success": "Account successfully validated."}, status=200)
        return web.json_response({"error": "Tokens do not match."}, status=417)
