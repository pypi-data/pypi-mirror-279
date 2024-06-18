from typing import Optional

from langchain_community.chat_models import ChatOllama
from langchain_core.callbacks import CallbackManager, StreamingStdOutCallbackHandler
from langchain_core.language_models import BaseChatModel
from langchain_openai import ChatOpenAI


def build_llm_proxy(model: str,
                    url: str,
                    engine: str,
                    temperature: float = 0.,
                    api_key: Optional[str] = None,
                    org_id: Optional[str] = None,
                    ) -> BaseChatModel:
    """
    Build a LLM proxy to use in a chain.
    :param temperature: parameter for generation
    :param org_id: To be passed to the underlying server if provided. Mostly of OpenAI
    :param api_key: To be passed to the underlying server if provided
    :param model: LLM name. I.e. mistral
    :param url: to the endpoint of the LLM server
    :param engine: LLM server type. I.e. Ollama, vLMM, TGI, OpenAI, etc.
    :return: The instance to the LLM proxy with the correct type and parameters
    """
    match engine.lower():
        case 'ollama':
            return ChatOllama(
                base_url=url,
                model=model,
                temperature=temperature,
                callback_manager=CallbackManager([StreamingStdOutCallbackHandler()])
            )
        case 'openai':
            return ChatOpenAI(
                base_url=url,
                model=model,
                temperature=temperature,
                openai_api_key=api_key,
                openai_organization=org_id,
                callback_manager=CallbackManager([StreamingStdOutCallbackHandler()])
            )
        case default:
            raise NotImplementedError(f"Unsupported \"{engine}\" LLM engine")

