# -*- coding: utf-8 -*-

from marshmallow import Schema, fields


class User(Schema):
    """Defines a MongoDB document for a single user.

    Attributes
    -----------
    name : str
        What is their name?
    major : str
        What is their major?
    age : str
        How old are they?
    token : str
        Used for email validation.
    is_validated : bool
        Once the user has clicked the link in their verification email, this will be true.
        Link will consist of their id (MongoDB generated) in /post/new/user and their token.
        Validation occurs at /get/validation via URL arguments.
    username : str
        What's their username?
    email : str
        What's their email?
    password : str
        What's their password?

    Notes
    ------
    Need to add validation of fields per https://marshmallow.readthedocs.io/en/3.0/quickstart.html#validation
    """
    name = fields.Str()
    major = fields.Str()
    age = fields.Integer()
    token = fields.Str()
    is_validated = fields.Boolean()
    username = fields.Str()
    email = fields.Str()
    password = fields.Dict(keys=fields.Str(), values=fields.Str()) # key is either salt or password, key is that value
