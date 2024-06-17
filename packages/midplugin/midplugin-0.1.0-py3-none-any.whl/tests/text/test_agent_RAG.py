import sys,os
import yaml
sys.path.append(os.getcwd())
import os
import logging
from nlpbridge.persistent.redis import RedisDB
from typing import(
    Any,List,
)
from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import BaseMessage
from langchain_openai import ChatOpenAI
from nlpbridge.langchain_zhipuai import ZhipuAIEmbeddings
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_community.vectorstores import Redis
from langchain.retrievers.multi_query import MultiQueryRetriever


os.environ["ZHIPUAI_API_KEY"] = "59e910acc5d4d68b9ef544009d89198d.mUfSMG5h6xgTphfL"
YAML_PATH= "/Users/apple/vitalis/source_code/midplugin/config.yaml"

with open(YAML_PATH, 'r') as file:
    config = yaml.safe_load(file)

redis = config['redis']
redis["redis_url"] = f"redis://default:{redis['password']}@{redis['url']}:{redis['port']}/{redis['db']}"
os.environ["REDIS_URL"] = redis['redis_url']

url = 'https://zh.wikipedia.org/wiki/Google'
def load_blog(url:str)->List[Document]:
    # Load blog post
    loader = WebBaseLoader(url)
    data = loader.load()

    # Split
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=0)
    splits = text_splitter.split_documents(data)
    return splits

def  redis_vector(docs:List[Document])->Redis:
    return Redis(redis_url=os.getenv('REDIS_URL'),
                 index_name=config['os_config']["RAG_GOOGLE_INDEX_NAME"],
                 embedding=ZhipuAIEmbeddings()
                 ).from_documents(documents=docs,embedding=ZhipuAIEmbeddings())


llm =  ChatOpenAI(api_key=config['chatgpt']['api_key'],base_url=config['chatgpt']['url'],temperature=0)
retriever_from_llm = MultiQueryRetriever.from_llm(
    retriever=redis_vector(load_blog(url)).as_retriever(), llm=llm
)

logging.basicConfig()
logging.getLogger("langchain.retrievers.multi_query").setLevel(logging.ERROR)

for _ in iter(int,1):
    user_input = input("Input: ")
    unique_docs = retriever_from_llm.invoke(user_input)
    print("\nOutput: ",unique_docs[0].page_content)
