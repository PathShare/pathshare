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


    async def is_duplicate_email(self, email: str) -> bool:
        """Make sure that the email does not already exist in the database.
        Use MongoDB's aggregation pipeline operators to do this quickly.
        Group by email and count how many of each email exist. If counted result
        is equal to 1, reject the POST.

        Parameters
        ----------
        email : str
            The email to be checked for.
        
        Returns
        -------
        bool
            True if the account already exists. False if it does not exist.
        """
        pipeline = [{"$group": {"_id": "$email", "count": {"$sum": 1}}}]
        seen = False
        async for document in self.client.users.aggregate(pipeline):
            if document.get("_id") == email:
                if document.get("count") == 1:
                    seen = True
                    break
        return seen