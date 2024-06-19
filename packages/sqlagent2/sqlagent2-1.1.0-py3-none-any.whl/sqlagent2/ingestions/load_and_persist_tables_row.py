import asyncio
import os
from typing import Dict

from sqlalchemy import create_engine, text

from llama_index.core import SQLDatabase, VectorStoreIndex
from llama_index.core.schema import TextNode
from llama_index.core.storage import StorageContext
from llama_index.embeddings.openai import OpenAIEmbedding, OpenAIEmbeddingModelType
from llama_index.vector_stores.pinecone import PineconeVectorStore
from pinecone import Pinecone

async def arun(
    max_row_index: int | None,
    sql_database: SQLDatabase,
    pinecone_api_key: str = os.getenv("PINECONE_API_KEY", ""),
    embedding_model=OpenAIEmbeddingModelType.TEXT_EMBED_3_SMALL,
    pinecone_host: str = os.getenv("PINECONE_HOST", ""),
    openai_api_key: str = os.getenv("OPENAI_API_KEY", ""),
) -> Dict[str, VectorStoreIndex]:
    """Index stock codes, stock names, and additional fields from stock_info table."""
    embedding_model = OpenAIEmbedding(api_key=openai_api_key, model=embedding_model)
    pc = Pinecone(api_key=pinecone_api_key, host=pinecone_host)
    pc_index = pc.Index(host=pinecone_host)
    stats = pc_index.describe_index_stats()
    indexed_tables = stats["namespaces"].keys()

    vector_index_dict = {}
    table_name = "stock_info"
    
    # create pinecone vector store, using namespace as table name
    pinecone_vector_store = PineconeVectorStore(
        pinecone_index=pc_index, namespace=table_name
    )
    # use pinecone store to save and load
    storage_context = StorageContext.from_defaults(
        vector_store=pinecone_vector_store,
    )
    print(f"Indexing rows in table: {table_name}")
    # if table index exists in namespace, skip
    if table_name in indexed_tables:
        print(f"Table {table_name} already indexed. Skipping.")
        vector_index_dict[table_name] = VectorStoreIndex.from_vector_store(
            vector_store=pinecone_vector_store, embed_model=embedding_model
        )
    else:
        # start indexing and generate embeddings
        engine = sql_database.engine
        with engine.connect() as conn:
            limit = f"LIMIT {max_row_index}" if max_row_index else ""
            cursor = conn.execute(text(f"""
                SELECT stock_code, stock_name, stock_name_kana, stock_name_en, short_name 
                FROM {table_name} {limit}
            """))
            result = cursor.fetchall()
            row_tups = [(row[0], row[1], row[2], row[3], row[4]) for row in result]

        # index each row, put into vector store index
        nodes = [
            TextNode(
                text=f"Stock Code: {t[0]}, Stock Name: {t[1]}, Stock Name Kana: {t[2]}, Stock Name EN: {t[3]}, Short Name: {t[4]}",
                id_=f"{table_name}{t[0]}"
            ) for t in row_tups
        ]

        # put into vector store index (use OpenAIEmbeddings by default)
        index = VectorStoreIndex(
            nodes=nodes,
            storage_context=storage_context,
            show_progress=True,
            embed_model=embedding_model,
        )

        # construct a dict of table name and index
        vector_index_dict[table_name] = index

    return vector_index_dict
