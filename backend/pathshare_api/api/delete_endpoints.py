# -*- coding: utf-8 -*-

import aiohttp

from aiohttp import web
from bson.objectid import ObjectId


class DeleteEndpoints(object):
    """Encapsulates routes for all DELETE requests made to the API.
    
    Attributes
    ----------
    db : MongoConnection
        An instance of MongoConnection.
    
    Notes
    -----
    Example update_ride call: localhost:5002/delete/user?id=SOME_USER'S_ID
    Example update_ride call: localhost:5002/delete/ride?id=SOME_RIDE'S_ID
    """
    def __init__(self, db):
        self.db = db


    async def delete_user(self, request: aiohttp.web_request.Request) -> web.json_response:
        """Delete an existing user
        
        Parameters
        -----------
        aiohttp.web_request.Request
            A request to the endpoint made by the frontend web client.

        Returns
        --------
        web.json_response
        Three types of JSON responses.
            The first occurs when the id key is missing. (Status 422 => Unprocessable Entity)
            The second occurs when a user does not exist. (Status 417 => Expectation Failed)
            The third occurs when the new user deletion request was successful. (Status 200 => OK)
        """
        _id = request.rel_url.query.get("id", None)
        if _id is None:
            return web.json_response({"error": "Please provide a user ID as a request argument (key=id)."}, status=422)

        try:
            user_id = ObjectId(_id)
        except Exception as e:
            return web.json_response({"error": f"User ID '{_id}'' is not valid. Exception: {e}"}, status=417)

        user = await self.db.client.users.find_one({"_id": user_id})
        if not user:
            return web.json_response({"error": f"There are no user with ID: {_id}."}, status=417)
        
        delete_result = await self.db.client.users.delete_one({"_id": user_id})
        if delete_result.acknowledged:
            return web.json_response({"success": f"Deleted user with ID: {_id}."}, status=200)
        return web.json_response({"error": f"Unable to delete user with ID: {_id}."}, status=417)


    async def delete_ride(self, request: aiohttp.web_request.Request) -> web.json_response:
        """Delete a ride from the system.
        
        Parameters
        -----------
        aiohttp.web_request.Request
            A request to the endpoint made by the frontend web client.

        Returns
        --------
        web.json_response
        Three types of JSON responses.
            The first occurs when the id key is missing. (Status 422 => Unprocessable Entity)
            The second occurs when the ride does not exist. (Status 417 => Expectation Failed)
            The third occurs when the ride deletion request was successful. (Status 200 => OK)
        """
        _id = request.rel_url.query.get("id", None)
        if _id is None:
            return web.json_response({"error": "Please provide a ride ID as a request argument (key=id)."}, status=422)

        try:
            ride_id = ObjectId(_id)
        except Exception as e:
            return web.json_response({"error": f"Ride ID '{_id}' is not valid. Exception: {e}"}, status=417)
      
        user = await self.db.client.rides.find_one({"_id": ride_id})
        if not user:
            return web.json_response({"error": f"There are no ride with ID: {_id}."}, status=417)
        
        delete_result = await self.db.client.rides.delete_one({"_id": ride_id})
        if delete_result.acknowledged:
            return web.json_response({"success": f"Deleted ride with ID: {_id}."}, status=200)
        return web.json_response({"error": f"Unable to delete ride with ID: {_id}."}, status=417)
       
