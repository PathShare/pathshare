# -*- coding: utf-8 -*-

"""Database connection for Pathshare"""

import os

import pymongo


class MongoConnection:
    """Connects to MongoDB Atlas cluster 'Pathshare-Cluster0'

    Attributes
    ----------
    db : pymongo.MongoClient.database
        The main database used for Pathshare. 
    """
    def __init__(self):
        USERNAME = os.environ.get("MONGO_USERNAME")
        PASSWORD = os.environ.get("MONGO_PASSWORD")
        uri = f"mongodb+srv://{USERNAME}:{PASSWORD}@pathshare-cluster0-j1oyz.mongodb.net/main"
        client = pymongo.MongoClient(uri)
        self.db = client.main

    
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

        return self.db.users.insert_one(data).inserted_id


if __name__ == "__main__":
    con = MongoConnection()
    print(con.test_insert("helAAAAlo"))