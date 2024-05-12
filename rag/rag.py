from langchain_community.document_loaders import *
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.vectorstores import VectorStore
from langchain_text_splitters import *
from langchain_together import ChatTogether
from langchain_together.embeddings import *
from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv

load_dotenv()


def load_docs_from_dir(dir_path: str, file_extension: str = 'md'):
    """
    Load documents from a directory with a specific file extension (default is markdown)
    """
    loader = DirectoryLoader(dir_path, glob=f'**/*.{file_extension}')
    return loader.load()


def load_docs(path: str):
    """
    Load documents from a specific file path
    """
    loader = UnstructuredMarkdownLoader(path)
    return loader.load()


# print(load_docs('../resources/specific_domain_knowledge_docs/state_of_the_union.md'))

def get_text_splitter_from_docs(docs: list[Document], chunk_size: int = 500, chunk_overlap: int = 0):
    """
    Split documents into chunks
    """
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return text_splitter.split_documents(docs)


def get_embedder():
    """
    Get the embeddings model
    """
    return TogetherEmbeddings(
        model="togethercomputer/m2-bert-80M-8k-retrieval"
    )


def get_vector_store(docs: list[Document], embeddings, index_name: str):
    """
    Get the vector store
    """
    return PineconeVectorStore.from_documents(docs, embeddings, index_name=index_name)


def get_retriever(vector_store: VectorStore, search_kwargs: dict):
    """
    Get the retriever
    """
    return vector_store.as_retriever(search_kwargs=search_kwargs)


def get_chat_chain(retriever):
    """
    Get the chat chain
    """

    def format_docs(docs):
        """
        Format the documents
        """
        return "\n\n".join([d.page_content for d in docs])

    template = """
    Answer the question based only on the following context:
    
    {context}
    
    Question: {question}
    """
    prompt = ChatPromptTemplate.from_template(template)
    return (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | ChatTogether()
            | StrOutputParser()
    )


def get_answer(question: str):
    """
    Get the answer to a question
    """
    docs = load_docs_from_dir('../resources/specific_domain_knowledge_docs', 'md')
    text_splitter = get_text_splitter_from_docs(docs)
    embeddings = get_embedder()
    vector_store = get_vector_store(text_splitter, embeddings, "subject-tutor")
    retriever = get_retriever(vector_store, search_kwargs={"k": 1})
    model = get_chat_chain(retriever)
    return model.invoke(question)
