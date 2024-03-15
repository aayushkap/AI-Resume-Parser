"""
Resume ingestion flow is described here.
"""

import os
from langchain.docstore.document import Document

from .embedding_utils import add_to_db
from ..file_operations import PDF_loader, DOCX_loader, add_row_to_csv

from ...config import resume_directory, info_directory, column_names, info_file_name
from ...services import api_call
from ...prompts import get_extract_info_prompt


def ingest_resume(file_name: str):

    file_path = os.path.join(resume_directory, file_name)

    if file_name.endswith(".docx"):
        resume = DOCX_loader(file_path)
    else:
        resume = PDF_loader(file_path)

    # Get the complete string content of the resume
    resume_content = ""

    for page in resume:
        resume_content += page.page_content

    try:
        prompt = get_extract_info_prompt()
        extracted_info = api_call(prompt, resume_content)
    except Exception as e:
        extracted_info = None
        print(f"Error extracting info for {file_name}: {e}")
        return False

    # Extracting information based on bullet points
    lines = extracted_info.split("\n")

    name = lines[0].split(". ")[1]
    experience = lines[1].split(". ")[1]
    education = lines[2].split(". ")[1]
    summary = ", ".join(lines[3].split(". ")[1:])

    row = [file_name, name, experience, education, summary]

    doc = Document(page_content=resume_content, metadata={"source": file_name})

    # Only add to csv, if adding to database is succesful
    if add_to_db(doc):
        return add_row_to_csv(
            os.path.join(info_directory, info_file_name),
            row,
            column_names,
        )
    else:
        return False
