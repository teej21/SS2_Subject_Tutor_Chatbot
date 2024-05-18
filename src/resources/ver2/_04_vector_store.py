from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from _03_embeddings_model import embeddings

loader = TextLoader("../specific_domain_knowledge_docs/state_of_the_union.md")
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=0)
docs = text_splitter.split_documents(documents)

from langchain_pinecone import PineconeVectorStore

index_name = "subject-tutor"

docsearch = PineconeVectorStore.from_documents(docs, embeddings, index_name=index_name)

retriever = docsearch.as_retriever(search_kwargs={"k": 1})

# docs = retriever.invoke("what did he say about ketanji brown jackson")

from langchain_together import ChatTogether
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

template = """Answer the question based only on the following context:

{context}

Question: {question}
"""
prompt = ChatPromptTemplate.from_template(template)
model = ChatTogether()


def format_docs(docs):
    return "\n\n".join([d.page_content for d in docs])


chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | model
        | StrOutputParser()
)

res = chain.invoke("what did he say about ketanji brown jackson")

print(res)
