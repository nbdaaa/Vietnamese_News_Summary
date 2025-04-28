import operator
from typing import Annotated
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from config.settings import OPENAI_API_KEY

llm = ChatOpenAI(
            model="gpt-4o",
            openai_api_key=OPENAI_API_KEY
        )
llm.invoke("Tôi tên là Đức Anh, bạn tên là gì")
