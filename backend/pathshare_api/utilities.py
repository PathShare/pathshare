# -*- coding: utf-8 -*-

"""Utility functions."""

import base64
import os
import smtplib

from uuid import uuid4
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import logme

from bson.json_util import dumps as bson_dump
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from pathshare_api.decorators import thread_task


async def get_fernet_token(salt: str) -> bytes:
	"""Create a fernet token/key for object symmetric encryption.
	
	Parameters
	----------
	salt : str
		Unique salt used in the derivation formula.
	
	Returns
	-------
	bytes
		The token used for symmetric decryption.
	"""
	# Setup the key deriviation formula
	derivation_formula = PBKDF2HMAC(
		algorithm=hashes.SHA256(),
		length=32,
		salt=bytes(salt.encode("utf-8")),
		iterations=100000,
		backend=default_backend(),
	)

	# Get the symmetric decryption key
	phrase = bytes(os.environ.get("GLOBAL_KEY").encode("utf-8"))

	# Derive the key using the key derviation formula
	return base64.urlsafe_b64encode(derivation_formula.derive(phrase))


async def encrypt_password(password: str) -> dict:
	"""Encrypt the plaintext password of a user registering an account.
	
	Parameters
	-----------
	password : str
		The plaintext password of the new account being created.
	
	Returns
	-------
	dict
		The salt and encrypted password of the account being created.
	"""
	# Get a token for encryption use
	salt = uuid4().hex
	token = await get_fernet_token(salt)
	
	# Initialize a new instance of Fernet, a symmetric encryption algorithm
	f = Fernet(token)

	# Encrypt the password using the key
	password = f.encrypt(bytes(password.encode("utf-8")))

	# Return the data for storage into database
	return dict(salt=salt, password=password.decode("ascii"))


async def decrypt_password(password_data: dict) -> str:
	"""Decrypt the encrypted password of a user attempting to login to
	their account.
	
	Parameters
	-----------
	password_data : dict
		The encrypted password and salt of the account attempting to login.
	
	Returns
	-------
	str
	   The plaintext password of the account logging in.
	"""
	# Get a token for decryption use
	token = await get_fernet_token(password_data.get("salt"))
	
	# Initialize a new instance of Fernet, a symmetric encryption algorithm
	f = Fernet(token)

	# Decrypt and return the password
	return f.decrypt(bytes(password_data.get("password").encode("utf-8"))).decode("ascii")


body = """
Hello {name},
Thank you for signing up for PathShare.

Please click the link below to verify your account.

Verification link: {link}

Sincerely,
The PathShare Team
"""


@logme.log
async def send_email(email: str, name: str, link: str, logger=None) -> None:
	"""Send an email to the prospective customer.
	Parameters
	----------
	email : str
		The email that was submitted.
	name : str
		The first name of the person who just registered.
	link : str
		The verification url for the person that just registered.
	logger : logme.LogmeLogger
		Logger instance injected by the logme module.
	""" 
	from_address = os.environ.get("EMAIL_USER")
	try:
		msg = MIMEMultipart()
		msg["From"] = from_address
		msg["To"] = email
		msg["Subject"] = "PathShare Email Verification"
		msg.attach(MIMEText(body.format(name=name.capitalize(), link=link), "plain"))
		server = smtplib.SMTP("smtp.gmail.com", 587)
		server.starttls()
		server.login(from_address, os.environ.get("EMAIL_PASS"))
		server.sendmail(from_address, [from_address, email], msg.as_string())
		server.quit()
	except Exception as e:
		logger.debug("An error occured when trying to send an email.")
		logger.exception(e)
