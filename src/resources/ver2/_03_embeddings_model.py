from langchain_cohere import CohereEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()

embeddings = CohereEmbeddings(cohere_api_key=os.environ["COHERE_API_KEY"])
