# Set up: https://www.mongodb.com/docs/v4.4/administration/install-community/
# MongoDB Python Drivers: pip install pymongo
# Run MongoDB on macOS: brew services start mongodb-community@4.4
# Local DB Connection in MongoDB VScode extension: mongodb://localhost

# Manages MongoDB database connection
from pymongo import MongoClient

db_client = MongoClient().local
