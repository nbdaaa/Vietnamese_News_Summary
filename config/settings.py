# config/settings.py

# LLM Provider Configuration
LLM_PROVIDER = "openai"  # Options: "openai", "google"

# API Keys
OPENAI_API_KEY = "OPENAI_API_KEY"  # Replace with your OpenAI API key
GOOGLE_API_KEY = "GOOGLE_API_KEY"  # Replace with your Google API key

# LLM Model Configuration
LLM_MODELS = {
    "openai": "gpt-4o", 
    "google": "gemini-2.0-flash"
}
LLM_MODEL = LLM_MODELS[LLM_PROVIDER]
LLM_TEMPERATURE = 0.2

# Cấu hình hệ thống
OUTPUT_FILE = "data/output/news_summaries.csv"

# Cấu hình crawling
MAX_ARTICLES = 10  # Số lượng bài báo tối đa cần crawl
CRAWL_DELAY = 1  # Thời gian chờ giữa các lần request (giây)
BATCH_SIZE = 5  # Số lượng URL crawl song song

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
    for j in range(1, 2):
        DEFAULT_URLS.append(f"https://vnexpress.net/{i}-p{j}")

# Cấu hình crawler
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'

# Trafilatura configuration
TRAFILATURA_INCLUDE_COMMENTS = False
TRAFILATURA_INCLUDE_TABLES = True
TRAFILATURA_INCLUDE_IMAGES = False
TRAFILATURA_INCLUDE_LINKS = False