from langchain_community.document_loaders import UnstructuredMarkdownLoader

markdown_path = '../specific_domain_knowledge_docs/demoData.md'

loader = UnstructuredMarkdownLoader(markdown_path)

data = loader.load()

print(data)


def get_data():
    return data
