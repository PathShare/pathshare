# -*- coding: utf-8 -*-

"""Database connection for Pathshare"""


class MongoConnection:
    """Connects to MongoDB Atlas cluster 'Pathshare-Cluster0'

    Attributes
    ----------
    client : motor.motor_asyncio.AsyncIOMotorClient()
        The main database used for Pathshare. 
    """
    def __init__(self, client):
        self.client = client

    
    def test_insert(self, message: str):
        """Insert a document into the database.

        Parameters
        -----------
        message : str
            The message to be inserted into the document.
        """
        data = {
            "pizza": message
        }

        yield from self.client.users.insert_one(data).inserted_id

