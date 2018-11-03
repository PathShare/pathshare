from marshmallow import Schema, fields
from datetime import datetime

class Ride(Schema):
    riders = fields.List(fields.Integer()) #Can change Integer to whatever Atlas uses for IDs
    departure_date = fields.DateTime()
    departure_location = fields.Dict(keys=fields.Str(), values=fields.Float()) #Ex: {"lat": 35.000241, "long": -106.346231}
    destination = fields.Dict(keys=fields.Str(), values=fields.Float())
    price_per_seat = fields.Integer()
    is_active = fields.Boolean()
