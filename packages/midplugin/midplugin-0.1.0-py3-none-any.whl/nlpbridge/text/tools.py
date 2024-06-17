"""
Base Tools
"""
import os
from langchain_community.vectorstores import Redis
from nlpbridge.langchain_zhipuai import ZhipuAIEmbeddings
from langchain_community.utilities import SerpAPIWrapper
from langchain_core.tools import BaseTool, Tool,tool
from langchain_core.documents import Document
from  typing import (
    Any,List,
)

os.environ["SERPAPI_API_KEY"] = "049114fb0f7c39bbd679a1e499723453c11a9bb25961767650d8ffde091609a1"
@tool("web_search")
def web_search(query: str) -> str:
    """A search engine. Useful for when you need to answer questions about current events. Input should be a search query."""
    search = SerpAPIWrapper()
    return search.run(query)

@tool
def rag_google(query: str)-> List[Document]:
    """Get google information from the local repository"""
    retriever = Redis(redis_url=os.getenv('REDIS_URL'),
                    index_name=os.getenv("RAG_GOOGLE_INDEX_NAME"),
                    embedding=ZhipuAIEmbeddings()
                    ).as_retriever()
    return retriever.invoke(input=query)

@tool
def multiply(x: float, y: float) -> float:
    """Multiply 'x' times 'y'."""
    return x * y

@tool
def subtract(x: float, y: float) -> float:
    """subtract 'x' and 'y'."""
    return x - y


@tool
def exponentiate(x: float, y: float) -> float:
    """Raise 'x' to the 'y'."""
    return x**y


@tool
def add(x: float, y: float) -> float:
    """Add 'x' and 'y'."""
    return x + y
