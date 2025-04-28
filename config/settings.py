# config/settings.py

# Cấu hình Google Gemini API
<<<<<<< HEAD
GOOGLE_API_KEY = "YOUR_GEMINI_API_KEY"  # Thay thế bằng API key thực của bạn
=======
GOOGLE_API_KEY = "YOUR_GEMINI_API_KEY"  # Thay thế bằng API key thực của bạn
>>>>>>> d1e749068105837a08fec2e954d01c0f694c5542

# Cấu hình hệ thống
OUTPUT_FILE = "data/output/news_summaries.csv"

# Cấu hình crawling
MAX_ARTICLES = 500  # Số lượng bài báo tối đa cần crawl
CRAWL_DELAY = 1  # Thời gian chờ giữa các lần request (giây)
BATCH_SIZE = 20 # Số lượng URL crawl song song

title = [
    'thoi-su', 
    'the-gioi', 
    'kinh-doanh', 
    'khoa-hoc-cong-nghe', 
    'bat-dong-san', 
    'suc-khoe', 
    'the-thao', 
    'giai-tri', 
    'phap-luat', 
    'giao-duc', 
    'doi-song', 
    'oto-xe-may', 
    'du-lich'
]

# Danh sách các URL mặc định để crawl
DEFAULT_URLS = []

for i in title:
    for j in range(1, 25):
        DEFAULT_URLS.append(f"https://vnexpress.net/{i}-p{j}")

# Cấu hình LLM (Gemini) - cố định
LLM_MODEL = "gemini-2.0-flash"
LLM_TEMPERATURE = 0.2

# Cấu hình crawler
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'

# Trafilatura configuration
TRAFILATURA_INCLUDE_COMMENTS = False
TRAFILATURA_INCLUDE_TABLES = True
TRAFILATURA_INCLUDE_IMAGES = False
TRAFILATURA_INCLUDE_LINKS = False
