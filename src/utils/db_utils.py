from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

"""
connect to the database
"""
db_uri = os.environ.get('MONGO_URI')
db_name = os.environ.get('MONGO_DB_NAME')
try:
    database = MongoClient(db_uri)[db_name]
except Exception as e:
    print(e)
    database = None


def add_new_users(user_data: dict):
    """
    add new users to the database
    """
    try:
        return database.users.insert_one(user_data)
    except Exception as e:
        return e


def get_user_by_username(username: str):
    """
    get a user from the database
    """
    try:
        user = database.users.find_one({'username': username})
        return user
    except Exception as e:
        print(e)
        return None
