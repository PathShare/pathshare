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
    """
    def __init__(self, db):
        self.db = db
    

    async def get_ride(request: aiohttp.web_request.Request):
        raise NotImplementedError


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
        _id = request.rel_url.query.get("id", None)
        if _id is None:
            return web.json_response({"error": "Please provide a user ID as a request argument."}, status=417)
        user_id = ObjectId(_id)
        data = await self.db.client.users.find_one({"_id": user_id})
        if not data:
            return web.json_response({"error": f"There are no user with ID: {_id}"}, status=417)
        data.pop("_id") # Remove redundant _id
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


    async def get_validation(request: aiohttp.web_request.Request):
        raise NotImplementedError
