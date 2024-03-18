# This file manages MongoDB database connection
# Set up: https://www.mongodb.com/docs/v4.4/administration/install-community/
# MongoDB Python Drivers: pip install pymongo
# Run MongoDB on macOS: brew services start mongodb-community@7.0
# Stop MongoDB on macOS: brew services stop mongodb-community@7.0
# Local DB Connection in MongoDB VScode extension: mongodb://localhost

from pymongo import MongoClient

db_client = MongoClient().local
