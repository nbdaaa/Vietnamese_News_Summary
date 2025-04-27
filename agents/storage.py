# agents/storage.py
import os
import pandas as pd
from typing import Dict, Any
from config.settings import OUTPUT_FILE
from agents import NewsProcessingState

def storage_agent(state: NewsProcessingState) -> Dict[str, Any]:
    """Agent chịu trách nhiệm lưu trữ kết quả"""
    results = state["results"]
    
    # Kiểm tra nếu đã xử lý hết URLs
    if not state["urls"]:
        # Tạo DataFrame và lưu thành CSV
        df = pd.DataFrame([(item["original"], item["summary"]) for item in results],
                          columns=["Original", "Summary"])
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
        
        # Save to CSV with UTF-8-SIG encoding for Excel compatibility
        df.to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig')
        
        print(f"Đã lưu {len(results)} bài báo vào file {OUTPUT_FILE}")
        return {"status": "completed_all", "next": "coordinator"}
    else:
        # Vẫn còn URLs cần xử lý
        next_url = state["urls"][0]
        remaining_urls = state["urls"][1:]
        
        return {"current_url": next_url, "urls": remaining_urls, "status": "processing", "next": "coordinator"}