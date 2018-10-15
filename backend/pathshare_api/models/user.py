from marshamallow import Schema, fields
from datetime import datetime

class User(Schema):
    name = fields.Str()
    major = fields.Str()
    age = fields.Integer()
    token = fields.Str()
    is_validated = fields.Boolean()
    username = fields.Str()
    email = fields.Str()
    password = fields.Dict(keys=fields.Str(), values=fields.Str()) #key is either salt or password, key is that value