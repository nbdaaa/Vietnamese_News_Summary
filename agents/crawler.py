# agents/crawler.py
import re
import requests
from bs4 import BeautifulSoup
from typing import TypedDict, List, Dict, Optional, Any
from config.settings import USER_AGENT, WEBSITE_SELECTORS
from agents import NewsProcessingState

def crawler_agent(state: NewsProcessingState) -> Dict[str, Any]:
    """Agent chịu trách nhiệm crawl nội dung bài báo"""
    current_url = state["current_url"]
    
    try:
        headers = {'User-Agent': USER_AGENT}
        response = requests.get(current_url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Xác định logic trích xuất nội dung dựa trên domain
        domain = re.search(r'https?://(?:www\.)?([^/]+)', current_url).group(1)
        
        # Sử dụng selectors từ cấu hình
        domain_key = next((k for k in WEBSITE_SELECTORS.keys() if k in domain), None)
        
        content = ""
        if domain_key:
            selectors = WEBSITE_SELECTORS[domain_key]
            content_div = soup.select_one(selectors["content_selector"])
            title_div = soup.select_one(selectors["title_selector"])
            
            title = title_div.get_text(strip=True) if title_div else "Không có tiêu đề"
            
            if content_div:
                # Loại bỏ các phần tử không cần thiết
                for tag in content_div.find_all(['figure', 'div.image', 'script']):
                    tag.decompose()
                
                # Trích xuất nội dung
                paragraphs = content_div.find_all('p')
                if paragraphs:
                    content = "\n\n".join([p.get_text(strip=True) for p in paragraphs])
                else:
                    content = content_div.get_text(strip=True)
                
                content = f"Tiêu đề: {title}\n\n{content}"
                return {"content": content, "status": "ready_for_summary", "next": "coordinator"}
            else:
                return {"errors": state["errors"] + [f"Không thể trích xuất nội dung từ {current_url}"], "status": "error", "next": "coordinator"}
        else:
            # Logic mặc định cho các trang khác
            title_tag = soup.find(['h1', 'h2.title'])
            title = title_tag.get_text(strip=True) if title_tag else "Không có tiêu đề"
            
            article = soup.find(['article', 'div.content', 'div.article-content'])
            if article:
                for tag in article.find_all(['figure', 'div.image', 'script']):
                    tag.decompose()
                
                paragraphs = article.find_all('p')
                if paragraphs:
                    content = "\n\n".join([p.get_text(strip=True) for p in paragraphs])
                else:
                    content = article.get_text(strip=True)
                
                content = f"Tiêu đề: {title}\n\n{content}"
                return {"content": content, "status": "ready_for_summary", "next": "coordinator"}
            else:
                return {"errors": state["errors"] + [f"Không thể trích xuất nội dung từ {current_url}"], "status": "error", "next": "coordinator"}
    
    except Exception as e:
        return {"errors": state["errors"] + [f"Lỗi khi crawl {current_url}: {str(e)}"], "status": "error", "next": "coordinator"}