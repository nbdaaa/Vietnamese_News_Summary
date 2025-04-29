# agents/crawler.py
import re
import requests
import trafilatura
from bs4 import BeautifulSoup
from typing import Dict, Any
from config.settings import USER_AGENT
from agents import NewsProcessingState

# Global counter for successful extractions
extraction_counter = 0

def remove_duplicated_content(text):
    """Xóa triệt để các câu và đoạn văn trùng lặp trong nội dung"""
    if not text:
        return ""
    
    # Chia thành các đoạn
    paragraphs = text.split('\n\n')
    
    # Phương pháp 1: Loại bỏ các đoạn hoàn toàn giống nhau
    unique_paragraphs = []
    seen_paragraphs = set()
    
    for paragraph in paragraphs:
        paragraph_stripped = paragraph.strip()
        if paragraph_stripped and paragraph_stripped not in seen_paragraphs:
            unique_paragraphs.append(paragraph)
            seen_paragraphs.add(paragraph_stripped)
    
    # Phương pháp 2: Kiểm tra và loại bỏ các đoạn giống nhau 
    # ngay cả khi chúng nằm ở vị trí khác nhau trong văn bản
    result_paragraphs = []
    processed_content = ""
    
    for paragraph in unique_paragraphs:
        # Chia thành các câu để xử lý chi tiết hơn
        sentences = re.split(r'(?<=[.!?])\s+', paragraph)
        unique_sentences = []
        
        for sentence in sentences:
            sentence = sentence.strip()
            # Chỉ thêm câu nếu nó chưa tồn tại trong nội dung đã xử lý
            # và có độ dài đủ để là một câu có ý nghĩa
            if (sentence and len(sentence) > 10 and 
                sentence not in processed_content and 
                not any(sentence in p for p in result_paragraphs)):
                unique_sentences.append(sentence)
                processed_content += sentence + " "
        
        # Nếu đoạn vẫn còn câu sau khi lọc
        if unique_sentences:
            result_paragraph = " ".join(unique_sentences)
            result_paragraphs.append(result_paragraph)
    
    # Ghép lại thành văn bản
    return '\n\n'.join(result_paragraphs)

def crawler_agent(state: NewsProcessingState) -> Dict[str, Any]:
    """Agent chịu trách nhiệm crawl nội dung bài báo"""
    current_url = state["current_url"]
    global extraction_counter
    
    try:
        # Kiểm tra nếu là URL video, bỏ qua
        if "video" in current_url or "/video/" in current_url:
            return {"errors": state["errors"] + [f"Bỏ qua URL video: {current_url}"], "status": "error", "next": "coordinator"}
        
        # Tải nội dung trang
        headers = {'User-Agent': USER_AGENT}
        response = requests.get(current_url, headers=headers, timeout=30)
        html_content = response.text
        
        # Phương pháp 1: Sử dụng Trafilatura
        content = trafilatura.extract(
            html_content, 
            include_comments=False, 
            include_tables=True,
            include_images=False, 
            include_links=False,
            favor_precision=True
        )
        
        if content and len(content) > 200:
            # Loại bỏ các đoạn trùng lặp
            content = remove_duplicated_content(content)
            extraction_counter += 1
            print(f"{extraction_counter}. Đã trích xuất thành công từ {current_url}")
            return {"content": content, "status": "ready_for_summary", "next": "coordinator"}
        
        # Phương pháp 2: Phương pháp dự phòng sử dụng BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Tìm tất cả đoạn văn trong trang
        all_paragraphs = soup.find_all('p')
        paragraphs_text = [p.get_text(strip=True) for p in all_paragraphs if len(p.get_text(strip=True)) > 20]
        
        if len(paragraphs_text) >= 3:  # Ít nhất 3 đoạn có ý nghĩa
            content = "\n\n".join(paragraphs_text)
            content = remove_duplicated_content(content)
            
            if len(content) > 200:
                extraction_counter += 1
                print(f"{extraction_counter}. Đã trích xuất thành công bằng phương pháp dự phòng từ {current_url}")
                return {"content": content, "status": "ready_for_summary", "next": "coordinator"}
        
        # Phương pháp 3: Thử phương pháp thứ ba - tìm nội dung trong các thẻ div phổ biến
        content_divs = soup.select('div.article-content, div.detail-content, div.article-body, div.content-detail, div.cms-body, div.article__body')
        if content_divs:
            content = "\n\n".join([div.get_text(strip=True) for div in content_divs])
            content = remove_duplicated_content(content)
            
            if len(content) > 200:
                extraction_counter += 1
                print(f"{extraction_counter}. Đã trích xuất thành công bằng phương pháp thứ ba từ {current_url}")
                return {"content": content, "status": "ready_for_summary", "next": "coordinator"}
        
        # Nếu trích xuất thất bại
        return {"errors": state["errors"] + [f"Không thể trích xuất nội dung từ {current_url}"], "status": "error", "next": "coordinator"}
    
    except Exception as e:
        return {"errors": state["errors"] + [f"Lỗi khi crawl {current_url}: {str(e)}"], "status": "error", "next": "coordinator"}