# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

setup(
	name="pathshare_api",
	version="1.0.0",
	description="Backend API for the Pathshare ridesharing platform.",
	packages=find_packages(),
	include_package_data=True,
	zip_safe=False,
)
