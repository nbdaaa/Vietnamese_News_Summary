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

# Define end agent
def end_agent(state: NewsProcessingState) -> NewsProcessingState:
    """End agent - does nothing, just returns the state"""
    return state

def build_workflow() -> StateGraph:
    """Build the workflow graph"""
    # Initialize graph
    workflow = StateGraph(NewsProcessingState)
    
    # Add nodes
    workflow.add_node("coordinator", coordinator_agent)
    workflow.add_node("crawl", crawler_agent)
    workflow.add_node("summarize", summarizer_agent)
    workflow.add_node("store", storage_agent)
    workflow.add_node("end", end_agent)

    # Define entry point
    workflow.set_entry_point("coordinator")

    # Define flow based on "next" value
    workflow.add_conditional_edges(
        "coordinator",
        lambda state: state.get("next", "crawl"),
        {
            "crawl": "crawl",
            "summarize": "summarize",
            "store": "store",
            "end": "end"
        }
    )

    # All nodes return to coordinator
    workflow.add_edge("crawl", "coordinator")
    workflow.add_edge("summarize", "coordinator")
    workflow.add_edge("store", "coordinator")
    
    # Compile graph
    return workflow.compile()

async def get_article_urls(urls: List[str], max_articles: int) -> List[str]:
    """Get article URLs from main pages with a maximum limit"""
    all_article_urls = []
    
    # Crawl main pages in parallel
    print(f"Crawling {len(urls)} main pages...")
    main_page_results = await parallel_crawler(urls)
    
    # Extract article URLs from each main page
    for result in main_page_results:
        if result["status"] == "success":
            domain = result["url"].split("/")[2]
            article_urls = extract_article_urls(result["html"], domain)
            
            all_article_urls.extend(article_urls)
            
            # Check if we have enough articles
            if len(all_article_urls) >= max_articles:
                break
    
    # Trim list if exceeds max_articles
    return all_article_urls[:max_articles]

def run_news_processing_system(urls: List[str]) -> Dict[str, Any]:
    """Run the news processing system"""
    # Build workflow
    workflow_app = build_workflow()
    
    if not urls:
        print("No URLs provided.")
        return {"status": "error", "results": [], "errors": ["No URLs provided."]}
    
    # Initialize state
    initial_state = {
        "urls": urls[1:],  # Remaining URLs
        "current_url": urls[0],  # First URL
        "content": None,
        "summary": None,
        "results": [],
        "errors": [],
        "status": "processing",
        "next": "coordinator"
    }
    
    # Display progress bar
    pbar = tqdm(total=len(urls), desc="Processing articles")
    last_count = 0
    
    # Execute workflow
    result = workflow_app.invoke(initial_state, {"recursion_limit": 10000000})
    
    # Update progress bar
    pbar.update(len(result['results']) - last_count)    
    pbar.close()
    
    # Report results
    print(f"\nProcessed {len(result['results'])} articles")
    print(f"Encountered {len(result['errors'])} errors")
    
    if result['errors']:
        print("Errors encountered:")
        for error in result['errors']:
            print(f"- {error}")
    
    print(f"Results saved to {os.path.abspath(result.get('output_file', 'news_summaries.csv'))}")
    
    return result

async def main():
    """Main function"""
    # Create command line argument parser
    parser = argparse.ArgumentParser(description='Crawl and summarize news articles')
    parser.add_argument('--urls', nargs='+', help='Main pages URLs (e.g., category pages)')
    parser.add_argument('--max', type=int, default=MAX_ARTICLES, help='Maximum number of articles to crawl')
    args = parser.parse_args()
    
    # Use URLs from command line or default
    main_urls = args.urls if args.urls else DEFAULT_URLS
    max_articles = args.max
    
    print(f"Collecting article URLs from {len(main_urls)} main pages...")
    print(f"Maximum number of articles to crawl: {max_articles}")
    
    try:
        # Get article URLs from main pages
        article_urls = await get_article_urls(main_urls, max_articles)
        
        print(f"Found {len(article_urls)} article URLs.")
        
        if not article_urls:
            print("No article URLs found. Check source pages.")
            return
            
        # Execute the system with article URLs
        run_news_processing_system(article_urls)
    except Exception as e:
        print(f"Error in main function: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Ensure output directory exists
    os.makedirs("data/output", exist_ok=True)
    
    try:
        # Run main() asynchronously with timeout
        asyncio.run(asyncio.wait_for(main(), timeout=3600))  # 1 hour timeout
    except asyncio.TimeoutError:
        print("Execution timed out.")
    except Exception as e:
        print(f"Error when running program: {str(e)}")
        import traceback
        traceback.print_exc()