# -*- coding: utf-8 -*-

"""Main module for the server of Pathshare's backend"""

import asyncio
import os

from aiohttp import web
from motor.motor_asyncio import AsyncIOMotorClient

from pathshare_api.controllers import MongoConnection
from pathshare_api.api import GetEndpoints

async def init_app() -> web.Application:
    """
    Initializes web application.

    Returns
    -------
    aiohttp.web.Application
         An initialized web application.
    """
    # Initialize fully async database client
    USERNAME = os.environ.get("MONGO_USERNAME")
    PASSWORD = os.environ.get("MONGO_PASSWORD")
    uri = f"mongodb+srv://{USERNAME}:{PASSWORD}@pathshare-cluster0-j1oyz.mongodb.net/main"
    client = AsyncIOMotorClient(uri).main
    
    # Initialize application and associate database
    app = web.Application()
    app["db"] = MongoConnection(client)
    
    # Add routes to application
    # Get routes are currently not implemented
    
    """
    app.router.add_get("/get/ride", GetEndpoints.get_ride)
    app.router.add_get("/get/user", GetEndpoints.get_user)
    app.router.add_get("/get/ride/all", GetEndpoints.get_all_rides)
    app.router.add_get("/get/validation/", GetEndpoints.get_validation)
    """
    return app


if __name__ == "__main__":
    web.run_app(init_app(), port=5002)