# -*- coding: utf-8 -*-

from marshmallow import Schema, fields


class Ride(Schema):
    """Defines a MongoDB document for a single ride.

    Attributes
    -----------
    riders : List[str]
        Who is going on the trip? List of MongoDB ObjectIds.
    departure_date : str
        When are they leaving? A string that will be converted into a Datetime object by dateutil.
    departure_location : str
        Where are they leaving from? This should be the name of a city. Frontend can parse lat-long if desired.
    destination : str
        Where are they going? This should be the name of a city. Frontend can parse lat-long if desired.
    price_per_seat : int
        How much is each person going to pay to carpool with the driver? Integers only for now.
    is_active : bool
        Is the ride in progress?

    Notes
    ------
    Need to add validation of fields per https://marshmallow.readthedocs.io/en/3.0/quickstart.html#validation
    """
    riders = fields.List(fields.Str())
    departure_date = fields.Str()
    departure_location = fields.Str()
    destination = fields.Str()
    price_per_seat = fields.Integer()
    is_active = fields.Boolean()
