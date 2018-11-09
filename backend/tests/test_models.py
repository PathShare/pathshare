# -*- coding: utf-8 -*-

"""Test suite for models defined in pathshare_api.models."""

import pytest

from datetime import datetime
from uuid import uuid4 # Used to generate tokens

from pathshare_api.models import Ride, User
from pathshare_api.utilities import encrypt_password

    
def test_ride_model() -> None:
    """Test that the Ride schema model is initialized correctly."""
    
    # Create a ride, use the departure location
    ride = dict(
        riders=[0, 1, 2, 3, 4, 5],
        departure_date=datetime.now(),
        departure_location="Lubbock",
        destination="Houston",
        price_per_seat=20,
        is_active=True,
    )

    # Initialize a ride_schema
    ride_schema = Ride()
    # Dump the ride data into the schema and extract the data
    result = ride_schema.dump(ride).data
    
    # Validate field types were created correctly
    for item in result:
        if item == "riders":
            assert type(result[item]) == list
        elif item == "departure_date":
            assert type(result[item]) == str
        elif item == "departure_location":
            assert type(item) == str
        elif item == "destination":
            assert type(item) == str
        elif item == "price_per_seat":
            assert type(result[item]) == int
        elif item == "is_active":
            assert type(result[item]) == bool
        

async def test_user_model() -> None:
    """Test that the User schema model is initialized correctly."""
    # Create a user, give them an encrypted password
    password = await encrypt_password("mysecurepassword")
    user = dict(
        name="John Doe",
        major="Computer Science",
        age="20",
        token=uuid4().hex,
        is_validated=False,
        username="jdoe",
        email="jdoe@ttu.edu",
        password=password
    )
    
    # Initialize a ride_schema
    user_schema = User()
    
    # Dump the ride data into the schema and extract the data
    result = user_schema.dump(user).data

    # Validate field types were created correted
    for item in result:
        if item == "name":
            assert type(result[item]) == str
        elif item == "major":
            assert type(result[item]) == str
        elif item == "age":
            assert type(result[item]) == int
        elif item == "token":
            assert type(result[item]) == str
        elif item == "is_validated":
            assert type(result[item]) == bool
        elif item == "username":
            assert type(result[item]) == str
        elif item == "password":
            assert type(result[item]) == dict
