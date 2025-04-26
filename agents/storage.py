# agents/storage.py
import os 
import pandas as pd
from typing import Dict, Any
from config.settings import OUTPUT_FILE
from agents import NewsProcessingState

def storage_agent(state: NewsProcessingState) -> Dict[str, Any]:
    """Agent chịu trách nhiệm lưu trữ kết quả"""
    results = state["results"]
    print(f"Storage: Xử lý {len(results)} kết quả, còn {len(state['urls'])} URL chưa xử lý")
    
    # Kiểm tra nếu đã xử lý hết URLs
    if not state["urls"]:
        # Tạo DataFrame và lưu thành CSV
        df = pd.DataFrame([(item["original"], item["summary"]) for item in results],
                          columns=["Original", "Summary"])
        
        output_file = OUTPUT_FILE
        print(f"Storage: Lưu kết quả vào {output_file}")
        # Đảm bảo thư mục tồn tại
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        df.to_csv(output_file, index=False, encoding='utf-8-sig')
        
        print("Storage: Hoàn thành, gửi trạng thái 'completed_all'")
        return {"status": "completed_all", "next": "coordinator"}
    else:
        # Vẫn còn URLs cần xử lý
        next_url = state["urls"][0]
        remaining_urls = state["urls"][1:]
        print(f"Storage: Tiếp tục với URL tiếp theo: {next_url}")
        
        return {"current_url": next_url, "urls": remaining_urls, "status": "processing", "next": "coordinator"}