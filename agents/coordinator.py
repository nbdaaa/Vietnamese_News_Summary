# agents/coordinator.py
from agents import NewsProcessingState
from typing import Dict, Any, Union

def coordinator_agent(state: NewsProcessingState) -> Dict[str, Any]:
    """Agent điều phối luồng công việc"""
    status = state["status"]
    print(f"Coordinator: Nhận trạng thái '{status}', next = {state.get('next', 'None')}")
    
    if status == "processing":
        print("Coordinator → Crawl")
        return {"next": "crawl"}
    elif status == "ready_for_summary":
        print("Coordinator → Summarize")
        return {"next": "summarize"}
    elif status == "completed_article":
        print("Coordinator → Store")
        return {"next": "store"}
    elif status == "completed_all":
        print("Coordinator → End")
        return {"next": "end"}
    elif status == "error":
        # Xử lý lỗi, có thể bỏ qua URL hiện tại và tiếp tục với URL tiếp theo
        if state["urls"]:
            next_url = state["urls"][0]
            remaining_urls = state["urls"][1:]
            print(f"Coordinator: Bỏ qua URL lỗi, chuyển sang URL tiếp theo: {next_url}")
            return {
                "current_url": next_url, 
                "urls": remaining_urls, 
                "errors": state["errors"], 
                "status": "processing",
                "next": "crawl"
            }
        else:
            print("Coordinator: Hết URL, hoàn thành")
            return {"next": "store"}