#!/usr/bin/python

"""Docker entrypoint for the deployed API."""

import os

from aiohttp import web
from dotenv import load_dotenv

from pathshare_api.main import init_app

os.chmod("pathshare_api/main.py", 0b111101101) # rwxr-xr-x 
load_dotenv()
app, _ = init_app()
web.run_app(app, port=80)
