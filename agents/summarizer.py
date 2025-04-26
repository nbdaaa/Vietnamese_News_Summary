# agents/summarizer.py
import os
from typing import Dict, Any
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from tenacity import retry, stop_after_attempt, wait_random_exponential
from agents import NewsProcessingState
from config.settings import LLM_MODEL, LLM_TEMPERATURE, GOOGLE_API_KEY

# Khởi tạo LLM Gemini
from langchain_google_genai import ChatGoogleGenerativeAI
llm = ChatGoogleGenerativeAI(
    model=LLM_MODEL,
    temperature=LLM_TEMPERATURE,
    google_api_key=GOOGLE_API_KEY
)

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def summarize_with_retry(content: str) -> str:
    """Tóm tắt nội dung với cơ chế thử lại"""
    prompt = ChatPromptTemplate.from_template(
        """Bạn là một chuyên gia tóm tắt bài báo Tiếng Việt.
        Hãy tóm tắt nội dung sau đây một cách súc tích, giữ lại các thông tin quan trọng,
        các sự kiện chính, và ý nghĩa của bài viết. Tóm tắt nên có độ dài khoảng 3-5 đoạn.
        
        Nội dung:
        {content}
        
        Tóm tắt:"""
    )
    
    chain = prompt | llm
    result = chain.invoke({"content": content})
    return result.content

def summarizer_agent(state: NewsProcessingState) -> Dict[str, Any]:
    """Agent chịu trách nhiệm tóm tắt nội dung"""
    content = state["content"]
    
    # Kiểm tra nếu nội dung quá dài, cần chia nhỏ
    if len(content) > 8000:
        # Chia nhỏ nội dung thành các phần
        splitter = RecursiveCharacterTextSplitter(chunk_size=4000, chunk_overlap=200)
        chunks = splitter.split_text(content)
        
        summaries = []
        # Tóm tắt từng phần
        for chunk in chunks:
            summary_chunk = summarize_with_retry(chunk)
            summaries.append(summary_chunk)
        
        # Tổng hợp các phần tóm tắt
        combined_summary = "\n\n".join(summaries)
        
        # Tóm tắt lại lần cuối
        final_prompt = ChatPromptTemplate.from_template(
            """Dưới đây là các phần tóm tắt của một bài báo dài.
            Hãy tổng hợp thành một bản tóm tắt nhất quán, súc tích và đầy đủ ý:
            
            {combined_summary}
            
            Tóm tắt cuối cùng:"""
        )
        final_chain = final_prompt | llm
        summary = final_chain.invoke({"combined_summary": combined_summary}).content
    else:
        # Tóm tắt trực tiếp nếu nội dung vừa phải
        summary = summarize_with_retry(content)
    
    # Lưu kết quả
    new_result = {"url": state["current_url"], "original": content, "summary": summary}
    updated_results = state["results"] + [new_result]
    
    return {"summary": summary, "results": updated_results, "status": "completed_article", "next": "coordinator"}