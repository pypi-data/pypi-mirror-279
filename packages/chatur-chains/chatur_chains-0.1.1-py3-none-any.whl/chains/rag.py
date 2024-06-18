""" Main RAG chain for Chatur """
from typing import Optional

from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, Runnable

from .llm_proxy import build_llm_proxy
from .retrieval import build_retriever, format_documents


def build_rag_chain(llm_host: str,
                    model_name: str,
                    llm_engine: str,
                    embeddings_engine: str,
                    api_key: Optional[str],
                    org_id: Optional[str],
                    vector_store: str,
                    temperature: float = 0.,
                    collection_name: str = "langchain",
                    embeddings_model: Optional[str] = None) -> Runnable:
    """
    Build a RAG chain for Chatur.
    :param embeddings_model: Name of the encoding transformer used to generate embeddings for dense retrieval
    :param embeddings_engine: Whether to use GPT4All, HuggingFace or OpenAI embeddings provider
    :param temperature: parameter for generation
    :param api_key: To the LLM server
    :param llm_engine: Type of LLM server to use
    :param org_id: For OpenAI connections
    :param llm_host: for the LLM server
    :param model_name: LLM model name
    :param vector_store: Path or connection string to VectorStore
    :param collection_name: in the vector store. Defaults to "langchain".
    :return: a Runnable object implementing RAG
    """

    prompt = ChatPromptTemplate.from_messages([
        HumanMessagePromptTemplate.from_template(
            """"You are a teaching assistant. Answer the student's question using information only and only from the 
            context passage that is between triple quotes. When you answer the question, quote the text that you used 
            to base your answer off. If you can't answer it, then say “I can't answer this question”.
    
            Context:
            ```{context}```"""

            "Question: {question}"
        ),
        # HumanMessagePromptTemplate.from_template(),
    ])

    llm = build_llm_proxy(model_name, llm_host, llm_engine, temperature, api_key, org_id)

    retriever = build_retriever(vector_store=vector_store,
                                collection_name=collection_name,
                                top_k=40,
                                embeddings_engine=embeddings_engine,
                                embeddings_model=embeddings_model)

    chain = (
            {"context": retriever | format_documents, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
    )

    return chain
