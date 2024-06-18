from pathlib import Path
from typing import Sequence, Optional

from langchain_core.documents import Document

from .embeddings import build_embeddings_provider
# from .vectordb_reader import VectorDBReader
import os

# weaviate connection info from environment
WEAVIATE_REST_HOST = os.environ.get('WEAVIATE_REST_HOST', 'localhost')
WEAVIATE_REST_PORT = os.environ.get('WEAVIATE_REST_PORT', '8080')
WEAVIATE_GRPC_HOST = os.environ.get('WEAVIATE_GRPC_HOST', 'localhost')
WEAVIATE_GRPC_PORT = os.environ.get('WEAVIATE_GRPC_PORT', '50051')
# WEAVIATE_API_KEY = os.environ.get('WEAVIATE_API_KEY', '')


def format_documents(docs: Sequence[Document]) -> str:
    """
    Formats document objects to make pass them into a prompt
    :param docs: Documents to format
    :return: a string with the formated documents
    """
    out_docs = "\n".join(doc.page_content for doc in docs)
    return out_docs


def build_retriever(vector_store: str,
                    top_k: int = 4,
                    collection_name: str = "langchain",
                    embeddings_engine: str = "GPT4All",
                    embeddings_model: Optional[str] = None):
    """ Factory function for creating a retriever instance to be used in a chain
        :param embeddings_model: Name of the transformer encoder user to generate sentence embeddings
        :param embeddings_engine: Name of the provider: GPT4All, HuggingFace or OpenAI
        :param vector_store: Path or connection string to the vector database provider. If a path is provided,
            it will be opened as a ChromaDB.
        :param top_k: Number of documents to retrieve. Default is 4.
        :param collection_name: Defaults to "langchain"
    """

    # Create the embeddings provider
    embeddings = build_embeddings_provider(embeddings_engine, embeddings_model)
    # if Path(vector_store).is_dir():
    #     # Use our Chroma wrapper
    #     vectorstore = VectorDBReader(db_path=vector_store,
    #                                  top_k=top_k,
    #                                  collection_name=collection_name,
    #                                  embeddings=embeddings)
    #     return vectorstore.as_retriever()
    if vector_store == "weaviate":
        import weaviate
        from langchain_weaviate.vectorstores import WeaviateVectorStore
        from weaviate.connect import ConnectionParams, ProtocolParams
        from weaviate.config import AdditionalConfig
        from weaviate.classes.config import Configure

        weaviate_conn_rest_config = ProtocolParams(host=WEAVIATE_REST_HOST, port=WEAVIATE_REST_PORT, secure=False)
        weaviate_conn_grpc_config = ProtocolParams(host=WEAVIATE_GRPC_HOST, port=WEAVIATE_GRPC_PORT, secure=False)
        weaviate_conn_params = ConnectionParams(http=weaviate_conn_rest_config, grpc=weaviate_conn_grpc_config)

        weaviate_client = weaviate.WeaviateClient(
            connection_params=weaviate_conn_params,
            # auth_client_secret=auth_cred,
            additional_config=AdditionalConfig(timeout=(5, 15)),  # connection timeout & read timeout time in seconds
        )
        try:
            weaviate_client.connect()
        except Exception as e:
            weaviate_client.close()
            raise e
        assert weaviate_client.is_ready()
        if not weaviate_client.collections.exists(collection_name):
            # data needs to be ingested first!
            raise NotImplementedError(f"Weaviate database does not contain collection: {collection_name}. Import data first.")
        vector_db = WeaviateVectorStore(client=weaviate_client, embedding=embeddings, text_key="text", index_name=collection_name, use_multi_tenancy=True)
        return vector_db.as_retriever()
    else:
        raise NotImplementedError(f"Vector store {vector_store} provider is not supported")
