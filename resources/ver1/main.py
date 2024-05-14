from dotenv import load_dotenv
from os import environ as os_environ
from Sentence import *
from Database import *

"""
load env variables
"""
load_dotenv()
INDEX_NAME = os_environ.get('INDEX_NAME')
MONGO_URI = os_environ.get('MONGO_URI')

"""
load database connection
"""

pinecone_index = load_index(INDEX_NAME)
mongo_client = connect_mongo(MONGO_URI)


def load_sentences(file_path):
    """
    load sentences from txt file
    """
    sentences_list = []
    with open(file_path, 'r') as file:
        for line in file:
            sentences_list.append(line.strip())
    return sentences_list


sentences = load_sentences('../../rag/specific_domain_knowledge_docs/demoData.md')

# print(sentences)
embeddings = generate_embeddings(sentences)


"""
sentense: "Hiện nay, trường đại học hà nội đang có hiệu trưởng là thầy Nguyễn Kim Sơn"
id: 434wefdsasdfdsfdfsdfda
values: [0.1, 0.2, 0.3, 0.4, 0.5]

--> promt-> vector -> query -> result -> id -> query from mongoDB by id

"""

def upsert_index(index_to_upsert, vectors):
    """
    upsert vectors to pinecone index
    """
    index_to_upsert.upsert(vectors=vectors)
    print("Upserted to Pinecone")


# upsert_index(pinecone_index, embeddings)


def insert_mongo(client, vectors):
    """
        insert vector id and original sentence to mongoDB
        """
    original_sentences = [{"id": vector["id"], "sentence": sentences[i]} for i, vector in enumerate(vectors)]
    client["sentence"]["sentence"].insert_many(original_sentences)
    print("Inserted to MongoDB")


# insert_mongo(mongo_client, embeddings)


promt = "Ai là hiệu trưởng trường đại học hà nội"

"""
promt -> vector -> query -> result -> id -> query from mongoDB by id

"""

embedding = generate_embedding(promt)
#
result = pinecone_index.query(vector=embedding, top_k=3, include_values=False)
#
# print(result)
# # query from mongoDB by id
result_sentences = []
for res in result['matches']:
    sentence = mongo_client["SS2"]["Sentences"].find_one({"id": res["id"]})
    print(sentence)
