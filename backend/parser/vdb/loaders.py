from langchain_community.document_loaders import PyPDFLoader


def PDF_loader(file_path):

    documents = []
    try:
        loader = PyPDFLoader(file_path)
        pages = loader.load()

        documents.extend(pages)

    except Exception as e:
        print(f"Error loading {file_path}: {e}")

    return documents


def DOCX_loader(file_path):

    return "documents"
