"""
Creating & storing vectors in a PostgreSQL database
"""

from langchain_community.vectorstores.pgvector import PGVector
from langchain.docstore.document import Document

from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModel

import torch.nn.functional as F
from torch import Tensor

from ...config import (
    postgresql_connection_string,
    postgresql_collection_name,
    huggingface_model,
    k_documents,
)


def average_pool(last_hidden_states: Tensor, attention_mask: Tensor) -> Tensor:
    last_hidden = last_hidden_states.masked_fill(~attention_mask[..., None].bool(), 0.0)
    return last_hidden.sum(dim=1) / attention_mask.sum(dim=1)[..., None]


def add_to_db(doc: Document) -> None:
    try:
        input_texts = [f"query: {doc.page_content}"]
        input_metadata = [doc.metadata]

        tokenizer = AutoTokenizer.from_pretrained(huggingface_model)
        model = AutoModel.from_pretrained(huggingface_model)

        # ? Tokenize the input texts
        batch_dict = tokenizer(
            input_texts,
            padding=True,
            truncation=True,
            return_tensors="pt",
        )

        outputs = model(**batch_dict)
        embeddings = average_pool(
            outputs.last_hidden_state, batch_dict["attention_mask"]
        )
        embeddings = F.normalize(embeddings, p=2, dim=1)

        db = PGVector(
            collection_name=postgresql_collection_name,
            connection_string=postgresql_connection_string,
            embedding_function=embeddings,
            pre_delete_collection=False,
        )

        db.add_embeddings(
            texts=input_texts, metadatas=input_metadata, embeddings=embeddings
        )

        return True

    except Exception as e:
        print(f"Error adding to db: {e}")
        return False


def query_vdb(query: str):

    model = SentenceTransformer("intfloat/multilingual-e5-small")

    embeddings = model.encode(query, normalize_embeddings=True)

    db = PGVector(
        collection_name=postgresql_collection_name,
        connection_string=postgresql_connection_string,
        embedding_function=embeddings,
    )

    similar_documents = db.similarity_search_with_score_by_vector(
        embeddings, k=k_documents
    )

    return similar_documents
