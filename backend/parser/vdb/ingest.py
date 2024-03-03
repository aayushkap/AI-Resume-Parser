"""
Resume ingestion flow is described here.
"""

import os
from langchain.docstore.document import Document

from .embedding_utils import add_to_db
from .loaders import PDF_loader, DOCX_loader


def ingest_resumes():
    # List of documents to be added to the database
    documents = []
    for filename in os.listdir("./data/resumes"):

        file_path = os.path.join("./data/resumes", filename)

        if filename.endswith(".docx"):
            resume = DOCX_loader(file_path)
        else:
            resume = PDF_loader(file_path)

        # Get the complete content of the resume
        resume_content = ""

        for page in resume:
            resume_content += page.page_content

        doc = Document(page_content=resume_content, metadata={"source": filename})
        documents.append(doc)

    add_to_db(documents)
