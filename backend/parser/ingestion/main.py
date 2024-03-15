"""
Entry point for the parser. Always run from here, so python understands project structure.

1. Accept files to ingest in the frontend.
2. Send to backend. Keep track of file names.
3. Save those files in directory.
4. Run extract info and ingestion process for only those files.

"""

import os
import pandas as pd
import shutil

from ..config import (
    resume_directory,
    data_directory,
    info_directory,
    info_file_name,
    column_names,
    postgresql_embedding_table,
    postgresql_collection_table,
)
from .vdb.ingest import ingest_resume
from .file_operations import read_csv
from .db_operations import clear_table


def save_and_ingest_file(contents: bytes, file_name: str):

    print(f"Attepting to Ingest File: {file_name}")

    if os.path.exists(os.path.join(info_directory, info_file_name)):
        df = read_csv(os.path.join(info_directory, info_file_name))

        if file_name in df[column_names[0]].values:
            print("Row with the same filename already exists.")
            return False

    # Create the upload directory if it doesn't exist
    if not os.path.exists(resume_directory):
        os.makedirs(resume_directory)

    file_path = os.path.join(resume_directory, file_name)

    # Save the file to disk
    with open(file_path, "wb") as file_object:
        file_object.write(contents)

    # Ingest the file
    return ingest_resume(file_name)


def get_all_resumes():
    resumes = []
    if os.path.exists(os.path.join(info_directory, info_file_name)):
        df = read_csv(os.path.join(info_directory, info_file_name))

        for filename in df[column_names[0]]:
            print(filename)
            resumes.append(filename)

    return resumes


def reset_parser_data():
    try:
        # Delete the folder if it exists
        if os.path.exists(data_directory):

            shutil.rmtree(data_directory)
            print(f"Folder '{data_directory}' and its contents deleted successfully.")

            # Create the folder again
            os.makedirs(data_directory)
            os.makedirs(info_directory)
            os.makedirs(resume_directory)
            print(f"Folder '{data_directory}' created successfully.")

        clear_table(postgresql_collection_table)
        clear_table(postgresql_embedding_table)
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
