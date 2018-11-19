# -*- coding: utf-8 -*-

"""Main module for the server of Pathshare's backend."""

import asyncio
import os
from typing import Tuple

import aiohttp_cors

from aiohttp import web
from motor.motor_asyncio import AsyncIOMotorClient

from pathshare_api.controllers import MongoConnection
from pathshare_api.api import DeleteEndpoints, GetEndpoints, PatchEndpoints, PostEndpoints


def init_app() -> Tuple[web.Application, AsyncIOMotorClient]:
    """
    Initializes the web application.

    Returns
    -------
    Tuple[web.Application, AsyncIOMotorClient]
    aiohttp.web.Application
        An initialized AIOHTTP web application.
    motor.motor_asyncio.AsyncIOMotorClient
        An async connection to the MongoDB Atlas cluster.
    """
    # Initialize fully async database client
    USERNAME = os.environ.get("MONGO_USERNAME")
    PASSWORD = os.environ.get("MONGO_PASSWORD")
    uri = f"mongodb+srv://{USERNAME}:{PASSWORD}@pathshare-cluster0-j1oyz.mongodb.net/main"
    client = AsyncIOMotorClient(uri).main
    
    # Initialize application and database
    app = web.Application()
    cors = aiohttp_cors.setup(app)
    db = MongoConnection(client)
    
    # Initialize endpoint classes
    gets = GetEndpoints(db)
    posts = PostEndpoints(db)
    patches = PatchEndpoints(db)
    deletes = DeleteEndpoints(db)
    
    # Add routes to application with CORS enabled
    # GET routes
    app.router.add_get("/", gets.home) # Default home
    app.router.add_get("/get/ride", gets.get_ride)
    app.router.add_get("/get/user", gets.get_user)
    app.router.add_get("/get/ride/all", gets.get_all_rides)
    app.router.add_get("/get/validation", gets.get_validation)
    
    # POST routes
    app.router.add_post("/post/user/new", posts.post_new_user)
    app.router.add_post("/post/ride/new", posts.post_new_ride)

    # PATCH routes
    app.router.add_patch("/patch/ride/{ride_id}/add/rider/{rider_id}", patches.add_rider)
    app.router.add_patch("/patch/ride/{ride_id}/delete/rider/{rider_id}", patches.remove_rider)

    # DELETE routes
    app.router.add_delete("/delete/user", deletes.delete_user)
    app.router.add_delete("/delete/ride", deletes.delete_ride)

    # Enable unrestricted CORS on all routes
    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True,
                expose_headers="*",
                allow_headers="*",
            )
    })

    for route in list(app.router.routes()):
        cors.add(route)
    
    return app, db


if __name__ == "__main__":
    app, _ = init_app()
    web.run_app(app, port=80)