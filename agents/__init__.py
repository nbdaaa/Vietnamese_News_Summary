# agents/__init__.py
from typing import TypedDict, List, Dict, Optional

class NewsProcessingState(TypedDict):
    urls: List[str]  # Danh sách URL cần crawl
    current_url: Optional[str]  # URL đang xử lý
    content: Optional[str]  # Nội dung đã crawl
    summary: Optional[str]  # Bản tóm tắt
    results: List[Dict[str, str]]  # Kết quả tổng hợp
    errors: List[str]  # Các lỗi gặp phải
    status: str  # Trạng thái hiện tại