import os
import csv
import pandas as pd

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import Docx2txtLoader


def PDF_loader(file_path: str):

    documents = []
    try:
        loader = PyPDFLoader(file_path)
        pages = loader.load()

        documents.extend(pages)

    except Exception as e:
        print(f"Error loading {file_path}: {e}")

    return documents


def DOCX_loader(file_path: str):
    documents = []
    try:
        loader = Docx2txtLoader(file_path)
        pages = loader.load()

        documents.extend(pages)
    except Exception as e:
        print(f"Error loading {file_path}: {e}")

    return documents


def write_file_to_path(path, contents):
    with open(path, "wb") as file_object:
        file_object.write(contents)
    return True


def add_row_to_csv(file_path: str, row_data: list, column_names: list) -> bool:
    try:
        if not os.path.exists(file_path):
            print(f"Creating: {file_path}")
            with open(file_path, "w", newline="") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(column_names)
        else:
            print(f"Appending to: {file_path}")

        with open(file_path, "a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(row_data)
        return True
    except Exception as e:
        print(f"Error adding row to CSV: {e}")
        return False


def read_csv(file_path: str) -> list:
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return None
