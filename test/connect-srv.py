from pymongo import MongoClient

from secret import MONGO_URL

client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=3000)
try:
    print(client.server_info())
except:
    print("Server not available")