# main.py
import os
import sys
import asyncio
import argparse
from typing import List, Dict, Any
from langgraph.graph import StateGraph
from tqdm import tqdm
from agents import NewsProcessingState
from agents.coordinator import coordinator_agent
from agents.crawler import crawler_agent
from agents.summarizer import summarizer_agent
from agents.storage import storage_agent
from utils.helpers import parallel_crawler, extract_article_urls
from config.settings import DEFAULT_URLS, MAX_ARTICLES

# Định nghĩa agent kết thúc
def end_agent(state: NewsProcessingState):
    """Agent kết thúc - không làm gì cả"""
    return state

def build_workflow() -> StateGraph:
    """Xây dựng đồ thị luồng công việc"""
    # Khởi tạo đồ thị
    workflow = StateGraph(NewsProcessingState)
    
    # Thêm các node
    workflow.add_node("coordinator", coordinator_agent)
    workflow.add_node("crawl", crawler_agent)
    workflow.add_node("summarize", summarizer_agent)
    workflow.add_node("store", storage_agent)
    workflow.add_node("end", end_agent)

    # Định nghĩa điểm bắt đầu 
    workflow.set_entry_point("coordinator")

    # Sửa lại cách xử lý điều kiện để tránh vòng lặp vô hạn
    # Kiểm tra giá trị "next" trong state
    workflow.add_conditional_edges(
        "coordinator",
        lambda state: state.get("next", "crawl"),  # Mặc định là "crawl" nếu không có "next"
        {
            "crawl": "crawl",
            "summarize": "summarize",
            "store": "store",
            "end": "end"
        }
    )

    # Đảm bảo rằng tất cả các node đều trả về cho coordinator
    workflow.add_edge("crawl", "coordinator")
    workflow.add_edge("summarize", "coordinator")
    workflow.add_edge("store", "coordinator")
    
    # Biên dịch đồ thị
    return workflow.compile()

async def get_article_urls(urls: List[str], max_articles: int) -> List[str]:
    """Lấy các URL bài viết từ các trang chính với giới hạn số lượng"""
    all_article_urls = []
    
    # Crawl song song các trang chính
    main_page_results = await parallel_crawler(urls)
    
    # Trích xuất các URL bài viết từ mỗi trang chính
    for result in main_page_results:
        if result["status"] == "success":
            domain = result["url"].split("/")[2]
            article_urls = extract_article_urls(result["html"], domain)
            
            all_article_urls.extend(article_urls)
            
            # Kiểm tra nếu đã đủ số lượng bài báo
            if len(all_article_urls) >= max_articles:
                break
    
    # Cắt bớt danh sách nếu vượt quá max_articles
    return all_article_urls[:max_articles]

def run_news_processing_system(urls: List[str]) -> Dict[str, Any]:
    """Chạy hệ thống xử lý tin tức"""
    # Xây dựng workflow với recursion_limit tăng lên
    workflow_app = build_workflow()
    
    if not urls:
        print("Không có URL nào được cung cấp.")
        return {"status": "error", "results": [], "errors": ["Không có URL nào được cung cấp."]}
    
    # Khởi tạo trạng thái
    initial_state = {
        "urls": urls[1:],  # URLs còn lại
        "current_url": urls[0],  # URL đầu tiên
        "content": None,
        "summary": None,
        "results": [],
        "errors": [],
        "status": "processing",
        "next": "crawl"  # Thay đổi từ "coordinator" thành "crawl"
    }
    
    # Hiển thị progress bar
    pbar = tqdm(total=len(urls), desc="Đang xử lý bài báo")
    last_count = 0
    
    # Thực thi luồng và cập nhật tiến trình với config recursion_limit cao hơn
    result = workflow_app.invoke(initial_state, {"recursion_limit": 1000})
    
    # Cập nhật progress bar
    pbar.update(len(result['results']) - last_count)
    pbar.close()
    
    # Báo cáo kết quả
    print(f"\nĐã xử lý {len(result['results'])} bài báo")
    print(f"Có {len(result['errors'])} lỗi")
    
    if result['errors']:
        print("Các lỗi gặp phải:")
        for error in result['errors']:
            print(f"- {error}")
    
    print(f"Kết quả đã được lưu vào file news_summaries.csv")
    
    return result

# main.py (phần hàm main())
async def main():
    """Hàm chính của chương trình"""
    try:
        # Tạo parser để xử lý tham số dòng lệnh
        parser = argparse.ArgumentParser(description='Crawl và tóm tắt bài báo')
        parser.add_argument('--urls', nargs='+', help='Các URL trang chính (ví dụ: trang danh mục báo)')
        parser.add_argument('--max', type=int, default=MAX_ARTICLES, help='Số lượng bài báo tối đa cần crawl')
        args = parser.parse_args()
        
        # Sử dụng URLs từ tham số dòng lệnh hoặc mặc định
        main_urls = args.urls if args.urls else DEFAULT_URLS
        max_articles = args.max
        
        print(f"Đang thu thập URL bài viết từ {len(main_urls)} trang chính...")
        print(f"Số lượng bài báo tối đa cần crawl: {max_articles}")
        
        # Lấy các URL bài viết từ trang chính
        print("Bắt đầu quá trình thu thập URL...")
        article_urls = await get_article_urls(main_urls, max_articles)
        
        print(f"Đã tìm thấy {len(article_urls)} URL bài viết.")
        
        if article_urls:
            # Thực thi hệ thống với các URL bài viết
            run_news_processing_system(article_urls)
        else:
            print("Không tìm thấy URL bài viết nào. Kiểm tra lại các trang nguồn.")
    except Exception as e:
        print(f"Lỗi trong hàm main: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Tạo thư mục output nếu chưa tồn tại
    os.makedirs("data/output", exist_ok=True)
    
    # Chạy hàm main() bất đồng bộ
    asyncio.run(main())