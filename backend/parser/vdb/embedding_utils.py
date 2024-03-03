"""
Creating & storing vectors in a PostgreSQL database
"""

from langchain_community.vectorstores.pgvector import PGVector
from langchain.docstore.document import Document

from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModel

import torch.nn.functional as F
from torch import Tensor

from config import (
    postgres_connection_string,
    postgres_collection_name,
    huggingface_model,
)


def average_pool(last_hidden_states: Tensor, attention_mask: Tensor) -> Tensor:
    last_hidden = last_hidden_states.masked_fill(~attention_mask[..., None].bool(), 0.0)
    return last_hidden.sum(dim=1) / attention_mask.sum(dim=1)[..., None]


def add_to_db(documents: list[Document]) -> None:

    input_texts = []
    input_metadata = []

    for doc in documents:
        input_texts.append(doc.page_content)
        input_metadata.append(doc.metadata)

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
    embeddings = average_pool(outputs.last_hidden_state, batch_dict["attention_mask"])
    embeddings = F.normalize(embeddings, p=2, dim=1)

    db = PGVector(
        collection_name=postgres_collection_name,
        connection_string=postgres_connection_string,
        embedding_function=embeddings,
        pre_delete_collection=True,
    )

    db.add_embeddings(
        texts=input_texts, metadatas=input_metadata, embeddings=embeddings
    )
