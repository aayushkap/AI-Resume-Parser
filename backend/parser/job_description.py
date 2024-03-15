"""

"""

import os
import pandas as pd

from .config import info_directory, info_file_name
from .ingestion.vdb.embedding_utils import query_vdb


def handle_user_query(query):

    df = pd.read_csv(os.path.join(info_directory, info_file_name))

    similar_documents = query_vdb(query)

    print(type(similar_documents))

    return similar_documents


"""if __name__ == "__main__":
    handle_user_query(
        "Financial Analyst with a MBA in Finance. Atleast 10 years of experience."
    )
else:
    handle_user_query(
        "Financial Analyst with a MBA in Finance. Atleast 10 years of experience."
    )
"""
