# utils/helpers.py
import asyncio
import aiohttp
import time
import re
from bs4 import BeautifulSoup
from config.settings import USER_AGENT, CRAWL_DELAY, BATCH_SIZE

async def parallel_crawler(urls, batch_size=BATCH_SIZE):
    """Crawl nhiều URL cùng lúc"""
    print(f"Đang crawl {len(urls)} URLs. Batch size: {batch_size}")
    results = []
    
    async def fetch_url(session, url):
        try:
            print(f"Bắt đầu tải {url}...")
            headers = {'User-Agent': USER_AGENT}
            async with session.get(url, headers=headers, timeout=30) as response:
                print(f"Đã nhận phản hồi từ {url}")
                html = await response.text()
                print(f"Đã tải xong nội dung từ {url}, kích thước: {len(html)} ký tự")
                # Thêm thời gian chờ để tránh bị chặn
                await asyncio.sleep(CRAWL_DELAY)
                return {"url": url, "html": html, "status": "success"}
        except Exception as e:
            print(f"Lỗi khi tải {url}: {str(e)}")
            return {"url": url, "html": None, "status": "error", "error": str(e)}
    
    # Xử lý theo batch
    for i in range(0, len(urls), batch_size):
        print(f"Xử lý batch {i//batch_size + 1}/{(len(urls)-1)//batch_size + 1}...")
        batch = urls[i:i+batch_size]
        async with aiohttp.ClientSession() as session:
            tasks = [fetch_url(session, url) for url in batch]
            batch_results = await asyncio.gather(*tasks)
            results.extend(batch_results)
    
    print(f"Đã hoàn thành việc crawl {len(results)} URLs")
    return results

def extract_article_urls(main_page_html, domain):
    """Trích xuất các URL bài viết từ trang chính"""
    print(f"Đang trích xuất URL từ trang {domain}, kích thước HTML: {len(main_page_html)} ký tự")
    soup = BeautifulSoup(main_page_html, 'html.parser')
    article_links = []
    
    # Regex để xác định URL bài viết hợp lệ
    article_pattern = re.compile(r'.*\.(html|htm)$|.*\/\d{4}\/\d{2}\/.*|.*\/[a-z0-9-]+_\d+\.html')
    
    if 'vnexpress.net' in domain:
        # Logic trích xuất URL bài viết cho VnExpress
        for link in soup.select('article h3.title-news a, .title-news a'):
            url = link.get('href')
            if url and url.startswith('http') and article_pattern.match(url):
                article_links.append(url)
    
    elif 'dantri.com.vn' in domain:
        # Logic trích xuất URL bài viết cho Dân Trí
        for link in soup.select('article h3.article-title a, .article-title a'):
            url = link.get('href')
            if url:
                if not url.startswith('http'):
                    url = f"https://dantri.com.vn{url}"
                if article_pattern.match(url):
                    article_links.append(url)
    
    else:
        # Logic mặc định
        for link in soup.find_all('a'):
            url = link.get('href')
            if url and ('article' in url or 'news' in url or 'bai-viet' in url or 'post' in url):
                if not url.startswith('http'):
                    if url.startswith('/'):
                        url = f"https://{domain}{url}"
                    else:
                        url = f"https://{domain}/{url}"
                if article_pattern.match(url):
                    article_links.append(url)
    
    # Loại bỏ các URL trùng lặp và các URL không phải bài viết
    unique_links = list(dict.fromkeys([url for url in article_links if is_valid_article_url(url, domain)]))
    print(f"Đã tìm thấy {len(unique_links)} URL bài viết hợp lệ từ {domain}")
    return unique_links

def is_valid_article_url(url, domain):
    """Kiểm tra xem URL có phải là URL bài viết hợp lệ không"""
    # Loại bỏ URL trang chủ, trang danh mục, trang tìm kiếm...
    invalid_patterns = [
        r'\/trang-chu\/?$', r'\/home\/?$', r'\/$', 
        r'\/category\/', r'\/tag\/', r'\/author\/', 
        r'\/search', r'\/tim-kiem', r'\/rss\/'
    ]
    
    for pattern in invalid_patterns:
        if re.search(pattern, url):
            return False
    
    # Chỉ giữ lại các URL có đường dẫn dài (URL bài viết thường có đường dẫn dài)
    path = url.split(domain, 1)[1] if domain in url else url
    return len(path.split('/')) >= 2