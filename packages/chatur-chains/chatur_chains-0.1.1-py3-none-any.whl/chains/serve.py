""" Server Wrapper for chains in this library """
import sys

from fastapi import FastAPI
from langchain.globals import set_debug
from langserve import add_routes

from chains.pdf_fixer import build_fix_pdf_chain
from chains.rag import build_rag_chain

app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="Spin up a simple api server using Langchain's Runnable interfaces",
)

set_debug(True)  # Comment out to remove debug messages

HOST = sys.argv[1]
PORT = int(sys.argv[2])
ENGINE = sys.argv[3]
API_KEY = sys.argv[4]
VECTORSTORE = sys.argv[5]
COLLECTION = sys.argv[6]
LLM_HOST = sys.argv[7]
MODEL = sys.argv[8]


# chain = build_rag_chain(LLM_HOST, MODEL, ENGINE, API_KEY, None, VECTORSTORE)
chain = build_fix_pdf_chain(LLM_HOST, MODEL, ENGINE, API_KEY, org_id=None)

add_routes(app, chain, path="/pdf-fixer")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=HOST, port=PORT)
