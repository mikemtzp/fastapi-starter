# This file manages MongoDB database connection
# Set up: https://www.mongodb.com/docs/v4.4/administration/install-community/
# MongoDB Python Drivers: pip install pymongo
# Run MongoDB on macOS: brew services start mongodb-community@7.0
# Stop MongoDB on macOS: brew services stop mongodb-community@7.0
# Local DB Connection in MongoDB VScode extension: mongodb://localhost

import os

from pymongo import MongoClient


# Remote DB
client = MongoClient(os.getenv("MONGODB_URI"))
# client = MongoClient("mongodb+srv://test:test@cluster0.kla9uuz.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

# Send a ping to confirm a successful connection
try:
    client.admin.command("ping")
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
