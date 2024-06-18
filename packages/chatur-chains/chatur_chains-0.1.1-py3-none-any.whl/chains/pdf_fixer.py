from typing import Optional

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_core.runnables import Runnable

from .llm_proxy import build_llm_proxy


def build_fix_pdf_chain(llm_host: str,
                        model_name: str,
                        llm_engine: str,
                        api_key: Optional[str],
                        org_id: Optional[str] = None,
                        temperature: float = 0.) -> Runnable:

    prompt = ChatPromptTemplate.from_messages([
        HumanMessagePromptTemplate.from_template(
            """"Clean the given text. Fix any typo, noises and spacing errors. Do not add new content.
            Raw text: ```{raw_text}```

            Clean text: """
        ),
        # HumanMessagePromptTemplate.from_template(),
    ])

    llm = build_llm_proxy(model_name, llm_host, llm_engine, temperature, api_key, org_id)

    chain = (
            prompt
            | llm
            | StrOutputParser()
    )

    return chain
