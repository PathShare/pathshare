# -*- coding: utf-8 -*-

import aiohttp
from aiohttp import web

class GetEndpoints(object):
    """Encapsulates routes for all GET requests made to the API."""

    async def get_ride(request: aiohttp.web_request.Request):
        raise NotImplementedError


    async def get_user(request: aiohttp.web_request.Request):
        raise NotImplementedError


    async def get_all_rides(request: aiohttp.web_request.Request):
        raise NotImplementedError


    async def get_validation(request: aiohttp.web_request.Request):
        raise NotImplementedError
