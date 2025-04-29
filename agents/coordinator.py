# agents/coordinator.py
from typing import Dict, Any
from agents import NewsProcessingState

def coordinator_agent(state: NewsProcessingState) -> Dict[str, Any]:
    """Agent điều phối luồng công việc"""
    status = state["status"]
    
    if status == "processing":
        return {"next": "crawl"}
    elif status == "ready_for_summary":
        return {"next": "summarize"}
    elif status == "completed_article":
        return {"next": "store"}
    elif status == "completed_all":
        return {"next": "end"}
    elif status == "error":
        # Xử lý lỗi, có thể bỏ qua URL hiện tại và tiếp tục với URL tiếp theo
        if state["urls"]:
            next_url = state["urls"][0]
            remaining_urls = state["urls"][1:]
            return {
                "current_url": next_url, 
                "urls": remaining_urls, 
                "errors": state["errors"], 
                "status": "processing",
                "next": "crawl"
            }
        else:
            return {"next": "store"}