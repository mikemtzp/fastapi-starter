# This file manages MongoDB database connection
# Set up: https://www.mongodb.com/docs/v4.4/administration/install-community/
# MongoDB Python Drivers: pip install pymongo

import os

from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

load_dotenv()

uri = os.getenv("MONGODB_CLUSTER0_URI")


client = MongoClient(uri, server_api=ServerApi("1"))


# Send a ping to confirm a successful connection
try:
    client.command("ping")
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
