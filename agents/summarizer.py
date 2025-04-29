# agents/summarizer.py
import os
from typing import Dict, Any
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from tenacity import retry, stop_after_attempt, wait_random_exponential
from agents import NewsProcessingState
from config.settings import LLM_PROVIDER, LLM_MODEL, LLM_TEMPERATURE, OPENAI_API_KEY, GOOGLE_API_KEY

# Initialize correct LLM based on provider
def initialize_llm():
    if LLM_PROVIDER == "google":
        # Google Gemini
        from langchain_google_genai import ChatGoogleGenerativeAI
        return ChatGoogleGenerativeAI(
            model=LLM_MODEL,
            temperature=LLM_TEMPERATURE,
            google_api_key=GOOGLE_API_KEY
        )
    elif LLM_PROVIDER == "openai":
        # OpenAI
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(
            model=LLM_MODEL,
            temperature=LLM_TEMPERATURE,
            openai_api_key=OPENAI_API_KEY
        )
    else:
        raise ValueError(f"Unsupported LLM provider: {LLM_PROVIDER}")

# Initialize LLM
llm = initialize_llm()

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def summarize_with_retry(content: str) -> str:
    """Summarize content with retry mechanism"""
    prompt = ChatPromptTemplate.from_template(
        """Bạn là một chuyên gia tóm tắt bài báo Tiếng Việt.
        Hãy tóm tắt nội dung sau đây một cách ngắn gọn, súc tích, giữ lại các thông tin quan trọng,
        các sự kiện chính, và ý nghĩa của bài viết. Chỉ nên tóm tắt bằng một đoạn văn bản duy nhất. 
        Lưu ý: Không được bắt đầu bằng "Bài viết này nói về" hoặc "Bài viết này đề cập đến" hoặc cách nói khác tương tự.
        
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

    try:
    
        # Check if content is too long and needs chunking
        if len(content) > 8000:
            # Split content into chunks
            splitter = RecursiveCharacterTextSplitter(chunk_size=4000, chunk_overlap=200)
            chunks = splitter.split_text(content)
            
            summaries = []
            # Summarize each chunk
            for chunk in chunks:
                summary_chunk = summarize_with_retry(chunk)
                summaries.append(summary_chunk)
            
            # Combine summaries
            combined_summary = "\n\n".join(summaries)
            
            # Final summarization of combined summaries
            final_prompt = ChatPromptTemplate.from_template(
                """Dưới đây là các phần tóm tắt của một bài báo dài.
                Hãy tổng hợp thành một bản tóm tắt nhất quán, súc tích và đầy đủ ý:
                
                {combined_summary}
                
                Tóm tắt cuối cùng:"""
            )
            final_chain = final_prompt | llm
            summary = final_chain.invoke({"combined_summary": combined_summary}).content
        else:
            # Summarize directly if content is moderate in length
            summary = summarize_with_retry(content)
        
        # Save result
        new_result = {"url": state["current_url"], "original": content, "summary": summary}
        updated_results = state["results"] + [new_result]
        
        return {"summary": summary, "results": updated_results, "status": "completed_article", "next": "coordinator"}
    
    except Exception as e:
        print(f"Error in summarization: {str(e)}")
        # Return original content as summary in case of API error
        return {
            "summary": f"[Error during summarization - using original content]\n\n{content[:500]}...", 
            "results": state["results"] + [{"url": state["current_url"], "original": content, "summary": content[:500] + "..."}],
            "status": "completed_article", 
            "next": "coordinator"
        }