# config/settings.py

# Cấu hình Google Gemini API (sử dụng cố định)
GOOGLE_API_KEY = "AIzaSyDhEoZMZUtgwc4o_BYY7EI9hywIfWWOuvQ"  # Thay thế bằng API key thực của bạn

# Cấu hình hệ thống
OUTPUT_FILE = "data/output/news_summaries.csv"

# Cấu hình crawling
MAX_ARTICLES = 300  # Số lượng bài báo tối đa cần crawl
CRAWL_DELAY = 1  # Thời gian chờ giữa các lần request (giây)
BATCH_SIZE = 3  # Số lượng URL crawl song song

# Danh sách các URL mặc định để crawl
DEFAULT_URLS = [
    "https://vnexpress.net/thoi-su-p1",
    "https://vnexpress.net/thoi-su-p2",
    "https://vnexpress.net/thoi-su-p3",
    #"https://dantri.com.vn/su-kien.htm",
]

# Cấu hình LLM (Gemini) - cố định
LLM_MODEL = "gemini-2.0-flash"
LLM_TEMPERATURE = 0.2

# Cấu hình crawler
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'

# Các selectors cho các trang web cụ thể
WEBSITE_SELECTORS = {
    "vnexpress.net": {
        "content_selector": "article.fck_detail",
        "title_selector": "h1.title-detail"
    },
    "dantri.com.vn": {
        "content_selector": "div.dt-news__content",
        "title_selector": "h1.title-page"
    },
}