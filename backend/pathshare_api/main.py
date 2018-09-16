# -*- coding: utf-8 -*-

"""Main module for the server of Pathshare's backend"""

import asyncio
from aiohttp import web
from pathshare_api.controllers import MongoConnection


async def init_app():
    """
    Initializes web application
    """
    app = web.Application()
    return app

web.run_app(init_app(), port=5002)