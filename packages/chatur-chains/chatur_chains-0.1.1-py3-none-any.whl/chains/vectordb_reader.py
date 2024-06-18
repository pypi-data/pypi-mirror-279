# -*- coding: utf-8 -*-

"""This module holds the vector database maintenance logic."""

from typing import Optional, Dict, Any

import weaviate
from langchain_community.vectorstores import Chroma  # pylint: disable=no-name-in-module
from langchain_core.embeddings import Embeddings
from langchain_core.vectorstores import VectorStoreRetriever
import chromadb
from langchain_weaviate import WeaviateVectorStore

from chains.embeddings import build_embeddings_provider


class VectorDBReader:
    """
    This class provide reader for a vector database, When constructing one, the path to the folder where the database
    will be persisted should be provided. If it isn't the database will not be
    persisted.
    """

    def __init__(self, db_path: Optional[str] = None,
                 collection_name: Optional[str] = None,
                 top_k: Optional[int] = None,
                 embeddings: Optional[Embeddings] = None,
                 engine: Optional[str] = None,
                 conf_kwargs: Optional[Dict[str, Any]] = None  # In the future support backend parameters through this
                 ):

        if conf_kwargs is None:
            conf_kwargs = dict()

        if embeddings:
            self._embedding = embeddings
        else:
            self._embedding = build_embeddings_provider("GPT4All")

        self._k_results = top_k
        self._db_path = db_path
        if collection_name:
            self._collection_name = collection_name
        else:
            self._collection_name = "langchain"

        if engine:
            engine = engine.lower()

        match engine:
            case "chroma" | None:
                client_settings = chromadb.Settings()
                if db_path:
                    client_settings.persist_directory = db_path
                    client_settings.is_persistent = True
                client = chromadb.Client(client_settings)
                self._impl = Chroma(
                    embedding_function=self._embedding,
                    client_settings=client_settings,
                    client=client,
                    collection_name=self._collection_name,
                )
            case "weaviate":
                client = weaviate.connect_to_local(**conf_kwargs)
                self._impl = WeaviateVectorStore(client=client,
                                                 index_name=self._collection_name,
                                                 embedding=self._embedding,
                                                 text_key="text")

    def as_retriever(self) -> VectorStoreRetriever:
        """Return VectorStoreRetriever initialized from this VectorStore."""

        # Set the configuration parameters of the retriever
        kw_args = {}
        # If k was specified, add it
        if self._k_results:
            kw_args['k'] = self._k_results

        # Unpack the kwargs
        return self._impl.as_retriever(search_kwargs=kw_args)
