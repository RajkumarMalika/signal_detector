import logging
from typing import List, Dict, Any
from playwright.sync_api import sync_playwright, TimeoutError

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def scrape_dynamic_web(url: str, source_name: str, item_selector: str, text_selector: str) -> List[Dict[str, Any]]:
    """
    Launches a headless browser to scrape dynamic JS-rendered websites.
    """
    logging.info(f"Launching Playwright to scrape: {url}")
    scraped_data = []

    with sync_playwright() as p:
        # 1. Launch a hidden (headless) browser
        browser = p.chromium.launch(headless=False)
        
        # 2. Set a standard User-Agent so websites don't block us as a basic bot
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0"
        )
        page = context.new_page()

        try:
            # 3. Go to the URL and wait for the network to calm down (meaning data loaded)
            page.goto(url, wait_until="domcontentloaded", timeout=15000)
            
            # 4. Wait for the specific HTML elements (like comments or reviews) to appear
            page.wait_for_selector(item_selector, timeout=10000)
            
            # 5. Grab all matching elements
            items = page.locator(item_selector).all()
            logging.info(f"Found {len(items)} matching items on {source_name}.")

            for item in items:
                # 6. Extract the actual text from inside the item
                text_element = item.locator(text_selector).first
                if text_element:
                    content = text_element.inner_text().strip()
                    
                    if content:
                        scraped_data.append({
                            "company_name": f"Unknown ({source_name})", 
                            "source_url": url,
                            "content": content
                        })

        except TimeoutError:
            logging.error(f"Timeout on {url}. The CSS selectors might be wrong or the page blocked us.")
        except Exception as e:
            logging.error(f"Scraping error: {e}")
        finally:
            browser.close() # Always close the browser to free up memory

    return scraped_data