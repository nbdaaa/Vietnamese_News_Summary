# utils/helpers.py
import asyncio
import aiohttp
import re
from bs4 import BeautifulSoup
from config.settings import USER_AGENT, CRAWL_DELAY, BATCH_SIZE

async def parallel_crawler(urls, batch_size=BATCH_SIZE):
    """Crawl nhiều URL cùng lúc"""
    results = []
    
    async def fetch_url(session, url):
        try:
            headers = {'User-Agent': USER_AGENT}
            async with session.get(url, headers=headers, timeout=30) as response:
                html = await response.text()
                # Thêm thời gian chờ để tránh bị chặn
                await asyncio.sleep(CRAWL_DELAY)
                return {"url": url, "html": html, "status": "success"}
        except Exception as e:
            print(f"Error fetching {url}: {str(e)}")
            return {"url": url, "html": None, "status": "error", "error": str(e)}
    
    # Xử lý theo batch
    for i in range(0, len(urls), batch_size):
        batch = urls[i:i+batch_size]
        print(f"Processing batch {i//batch_size + 1}/{(len(urls)-1)//batch_size + 1}...")
        async with aiohttp.ClientSession() as session:
            tasks = [fetch_url(session, url) for url in batch]
            batch_results = await asyncio.gather(*tasks)
            results.extend(batch_results)
    
    return results

def extract_article_urls(main_page_html, domain):
    """Trích xuất các URL bài viết từ trang chính"""
    soup = BeautifulSoup(main_page_html, 'html.parser')
    article_links = []
    
    # Regex để xác định URL bài viết hợp lệ
    article_pattern = re.compile(r'.*\.(html|htm)$|.*\/\d{4}\/\d{2}\/.*|.*\/[a-z0-9-]+_\d+\.html')
    
    # Regex để loại bỏ URL video
    video_pattern = re.compile(r'video\.|\.mp4|\/video\/')
    
    if 'vnexpress.net' in domain:
        # Logic trích xuất URL bài viết cho VnExpress
        for link in soup.select('article h3.title-news a, .title-news a, .title a, .item-news a'):
            url = link.get('href')
            if (url and url.startswith('http') and article_pattern.match(url) 
                and not video_pattern.search(url)):
                article_links.append(url)
    
    elif 'dantri.com.vn' in domain:
        # Logic trích xuất URL bài viết cho Dân Trí
        for link in soup.select('article h3.article-title a, .article-title a, .title a, .post-title a'):
            url = link.get('href')
            if url and not video_pattern.search(url):
                if not url.startswith('http'):
                    url = f"https://dantri.com.vn{url}"
                if article_pattern.match(url):
                    article_links.append(url)
    
    else:
        # Logic mặc định
        for link in soup.find_all('a'):
            url = link.get('href')
            if (url and ('article' in url or 'news' in url or 'bai-viet' in url or 'post' in url) 
                and not video_pattern.search(url)):
                if not url.startswith('http'):
                    if url.startswith('/'):
                        url = f"https://{domain}{url}"
                    else:
                        url = f"https://{domain}/{url}"
                if article_pattern.match(url):
                    article_links.append(url)
    
    # Loại bỏ các URL trùng lặp và các URL không phải bài viết
    unique_links = list(dict.fromkeys([url for url in article_links if is_valid_article_url(url, domain)]))
    print(f"Found {len(unique_links)} article URLs from {domain}")
    return unique_links

def is_valid_article_url(url, domain):
    """Kiểm tra xem URL có phải là URL bài viết hợp lệ không"""
    # Loại bỏ URL trang chủ, trang danh mục, trang tìm kiếm...
    invalid_patterns = [
        r'\/trang-chu\/?$', r'\/home\/?$', r'\/$', 
        r'\/category\/', r'\/tag\/', r'\/author\/', 
        r'\/search', r'\/tim-kiem', r'\/rss\/',
        r'video\.', r'\.mp4', r'\/video\/'  # Video patterns
    ]
    
    for pattern in invalid_patterns:
        if re.search(pattern, url):
            return False
    
    # Chỉ giữ lại các URL có đường dẫn dài (URL bài viết thường có đường dẫn dài)
    path = url.split(domain, 1)[1] if domain in url else url
    return len(path.split('/')) >= 2