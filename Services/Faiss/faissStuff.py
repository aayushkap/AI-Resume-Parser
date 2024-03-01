from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import OpenAIEmbeddings
import os
import warnings
import tiktoken
from langchain.schema import Document

import os

warnings.filterwarnings("ignore")

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
encoding = tiktoken.get_encoding("cl100k_base")


def embed_index(doc_list, filename, index_store):
    embed_fn = embeddings  # Assuming embeddings is defined elsewhere

    combined_content = ""
    for doc in doc_list:
        combined_content += doc.page_content

    combined_doc = Document(
        page_content=combined_content,
        metadata={"combined_pages": True, "source": filename},
    )

    try:
        faiss_db = FAISS.from_documents([combined_doc], embed_fn)
    except:
        faiss_db = FAISS.from_texts([combined_doc], embed_fn)

    if os.path.exists(index_store):
        local_db = FAISS.load_local(index_store, embed_fn)
        local_db.merge_from(faiss_db)
        print("Merging with existing index")
        local_db.save_local(index_store)
        print("Index saved")
    else:
        faiss_db.save_local(folder_path=index_store)
        print("New Index saved")


def get_pdf_splits(pdf_file):

    loader = PyPDFLoader(pdf_file)
    pages = loader.load()

    textSplit = RecursiveCharacterTextSplitter(
        chunk_size=1500, chunk_overlap=0, length_function=len
    )
    doc_list = []
    doc_list.extend(pages)  #! Look Into This

    return doc_list


def get_docs_length(index_path, embed_fn):
    test_index = FAISS.load_local(index_path, embed_fn)
    test_dict = test_index.docstore._dict
    return len(test_dict.values())


def testEmbeddings(query):
    if not os.path.exists("index_store"):
        print("Index does not exist")
        return None
    else:
        db = FAISS.load_local("index_store", embeddings)
        data_list = []  # List to store the results

        count = 0
        results_with_scores = db.similarity_search_with_score(
            query, k=get_docs_length("index_store", embeddings)
        )
        for doc, score in results_with_scores:
            count += 1
            # print(f"Content: {doc.page_content}, Metadata: {doc.metadata}, Score: {score}")
            source = doc.metadata.get("source", "N/A")
            data_list.append({"Metadata": doc.metadata, "Score": score})
        print("Number of Res: ", count)

        return data_list


"""
for filename in os.listdir("./Resumes"):
    file_path = os.path.join("./Resumes", filename)
    print(file_path)

    resume = get_pdf_splits(file_path)
    embed_index(resume, filename, "index_store")

print(testEmbeddings("Financial Analyst"))
"""
