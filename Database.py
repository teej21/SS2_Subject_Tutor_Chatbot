import dotenv
from pinecone import *
import os

from pinecone import Index
from pymongo import MongoClient

# load env
dotenv.load_dotenv()

'''
load index from Pinecone server
'''


def load_index(index_name: str) -> Index or None:
    try:
        # Initialize Pinecone
        pc = Pinecone(api_key=os.environ.get('PINECONE_API_KEY'))
        # Check if the index exists
        exist_index = False
        for result in pc.list_indexes():
            if result.name == index_name:
                print("Index already exists")
                exist_index = True
                break
        if not exist_index:
            print("Creating index")
            pc.create_index(
                name=index_name,
                dimension=384,
                metric="cosine",
                spec=ServerlessSpec(
                    cloud="aws",
                    region="us-east-1"
                )
            )
        # Connect to the index
        result = pc.Index(index_name)
        return result
    except Exception as e:
        print(e)
        return None


'''
connect to MongoDB
'''


def connect_mongo(mongo_uri: str) -> MongoClient or None:
    try:
        client = MongoClient(mongo_uri)
        return client
    except Exception as e:
        print(e)
        return None
