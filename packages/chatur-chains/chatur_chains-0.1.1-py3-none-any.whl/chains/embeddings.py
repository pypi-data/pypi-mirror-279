from typing import Optional

from langchain_community.embeddings import (
    GPT4AllEmbeddings, OpenAIEmbeddings, HuggingFaceEmbeddings
)
from langchain_core.embeddings import Embeddings


def build_embeddings_provider(engine: str, model: Optional[str] = None) -> Embeddings:
    engine = engine.lower().strip()

    match engine:
        case "gpt4all":
            if not model:
                model = "all-MiniLM-L6-v2.gguf2.f16.gguf"
            provider = GPT4AllEmbeddings(model_name=model)
        case "openai":
            if not model:
                model = "text-embedding-3-small"
            provider = OpenAIEmbeddings(model=model)
        case "huggingface":
            if not model:
                model = "sentence-transformers/all-MiniLM-L6-v2"
            provider = HuggingFaceEmbeddings(
                model_name=model
            )
        case _:
            raise NotImplementedError(f"Embedding engine \"{engine}\" is not yet supported.")

    return provider
