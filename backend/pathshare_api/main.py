# -*- coding: utf-8 -*-

"""Main module for the server of Pathshare's backend."""

import asyncio
import os

from aiohttp import web
from motor.motor_asyncio import AsyncIOMotorClient

from pathshare_api.controllers import MongoConnection
from pathshare_api.api import GetEndpoints, PostEndpoints

    
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
    
    # Initialize application and database
    app = web.Application()
    db = MongoConnection(client)
    
    # Initialize endpoint classes
    gets = GetEndpoints(db)
    posts = PostEndpoints(db)
    
    # Add routes to application
    # GET routes are currently not implemented
    # app.router.add_get("/get/ride", GetEndpoints.get_ride)
    app.router.add_get("/get/user", gets.get_user)
    app.router.add_get("/get/ride/all", gets.get_all_rides)
    # app.router.add_get("/get/validation/", GetEndpoints.get_validation)

    # POST routes
    app.router.add_post("/post/user/new", posts.post_new_user)
    app.router.add_post("/post/ride/new", posts.post_new_ride)
    return app


if __name__ == "__main__":
    web.run_app(init_app(), port=5002)