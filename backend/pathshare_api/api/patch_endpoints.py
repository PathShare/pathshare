# -*- coding: utf-8 -*-

import json
import os

import aiohttp

from aiohttp import web
from bson.objectid import ObjectId


class PatchEndpoints(object):
    """Encapsulates routes for all PATCH requests made to the API.
    
    Attributes
    ----------
    db : MongoConnection
        An instance of MongoConnection.

    Notes
    -----
    Example update_ride call: localhost:5002/patch/ride/SOME_RIDE_ID/add/rider/SOME_RIDER'S_ID
    Example remove_rider call: localhost:5002/patch/ride/SOME_RIDE_ID/delete/rider/SOME_RIDER'S_ID
    """
    def __init__(self, db):
        self.db = db


    async def add_rider(self, request: aiohttp.web_request.Request) -> web.json_response:
        """Add a rider to an existing ride.

        Parameters
        -----------
        aiohttp.web_request.Request
            A request to the endpoint made by the frontend web client.

        Returns
        --------
        web.json_response
        Four types of JSON responses.
            The first occurs when a ride does not exist or is in an invalid format. (Status 417 => Expectation Failed)
            The second occurs when a rider not exist or is in an invalid format. (Status 417 => Expectation Failed)
            The third occurs when a rider is already a member of a particular ride. (Status 417 => Expectation Failed)
            The fourth occurs when PUT request was successful. (Status 200 => OK)
        """
        ride_id = request.match_info.get("ride_id", None)
        rider_id = request.match_info.get("rider_id", None)
        
        try:
            ride_id = ObjectId(ride_id)
        except Exception as e:
            return web.json_response({"error": f"Ride ID {ride_id} is not valid. Exception: {e}"}, status=417)

        try:
            rider_id = ObjectId(rider_id)
        except Exception as e:
            return web.json_response({"error": f"User ID {rider_id} is not valid. Exception: {e}"}, status=417)

        find_ride = await self.db.client.rides.find_one({"_id": ride_id})
        if find_ride is None:
            return web.json_response({"error": f"Unable to find user with ID {ride_id}"}, status=417)
        
        find_rider = await self.db.client.users.find_one({"_id": rider_id})
        if find_rider is None:
            return web.json_response({"error": f"Unable to find ride with ID {rider_id}"}, status=417)

        new_riders = find_ride["riders"]
        if str(rider_id) in new_riders:
            return web.json_response({"error": f"Rider with ID {rider_id} is already a member of this ride"}, status=417)

        if new_riders is None:
            new_riders = []
        new_riders.append(str(rider_id))
        await self.db.client.rides.find_one_and_update({"_id": ride_id}, {"$set": {"riders": new_riders}})

        return web.json_response({"data": f"Successfully updated ride: {ride_id}. Added rider {rider_id}."}, status=200)


    async def remove_rider(self, request: aiohttp.web_request.Request) -> web.json_response:
        """Remove a rider to an existing ride.

        Parameters
        -----------
        aiohttp.web_request.Request
            A request to the endpoint made by the frontend web client.

        Returns
        --------
        web.json_response
        Four types of JSON responses.
            The first occurs when a ride does not exist or is in an invalid format. (Status 417 => Expectation Failed)
            The second occurs when a rider not exist or is in an invalid format. (Status 417 => Expectation Failed)
            The third occurs when a rider is not a member of a particular ride. (Status 417 => Expectation Failed)
            The fourth occurs when PUT request was successful. (Status 200 => OK)
        """
        ride_id = request.match_info.get("ride_id", None)
        rider_id = request.match_info.get("rider_id", None)
        
        try:
            ride_id = ObjectId(ride_id)
        except Exception as e:
            return web.json_response({"error": f"Ride ID {ride_id} is not valid. Exception: {e}"}, status=417)

        try:
            rider_id = ObjectId(rider_id)
        except Exception as e:
            return web.json_response({"error": f"User ID {rider_id} is not valid. Exception: {e}"}, status=417)
        
        find_ride = await self.db.client.rides.find_one({"_id": ride_id})
        if find_ride is None:
            return web.json_response({"error": f"Unable to find user with ID {ride_id}"}, status=417)
        
        find_rider = await self.db.client.users.find_one({"_id": rider_id})
        if find_rider is None:
            return web.json_response({"error": f"Unable to find ride with ID {rider_id}"}, status=417)

        current_riders = find_ride["riders"]
        if str(rider_id) not in current_riders:
            return web.json_response({"error": f"Rider with ID {rider_id} is not a member of this ride."}, status=417)

        current_riders.remove(str(rider_id))
        await self.db.client.rides.find_one_and_update({"_id": ride_id}, {"$set": {"riders": current_riders}})

        return web.json_response({"data": f"Successfully updated ride: {ride_id}. Removed rider {rider_id}."}, status=200)
