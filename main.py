import json
import os
import logging
from utils.ingestion import scrape_dynamic_web
from signals.competitor_grievance import process_grievance_signal

def main():
    logging.info("Starting Web Scraping Signal Pipeline...")
    
    # 1. Define targets and their specific HTML structure (CSS Selectors)
    # We will target a public HackerNews thread about hiring tools as a safe test
    sources = [
        {
            "name": "HackerNews Discussion (HackerRank Complaints)",
            # The CORRECT thread full of hiring tool grievances
            "url": "https://news.ycombinator.com/item?id=31094484", 
            "item_selector": ".comtr",        
            "text_selector": ".commtext"      
        }
    ]
    
    raw_data = []
    
    # 2. Ingest the Data
    for source in sources:
        data = scrape_dynamic_web(
            url=source["url"], 
            source_name=source["name"],
            item_selector=source["item_selector"],
            text_selector=source["text_selector"]
        )
        raw_data.extend(data)
        
    if not raw_data:
        logging.error("Pipeline aborted: No data scraped.")
        return
        
    detected_signals = []
    
    # 3. Process the Data
    # 3. Process the Data
    logging.info("Analyzing text for competitor grievances...")
    for record in raw_data:
        # ADD THIS LINE to see the raw text:
        print(f"\n--- SCRAPED TEXT ---\n{record['content']}\n--------------------\n")
        
        signal = process_grievance_signal(record)
        if signal:
            detected_signals.append(signal)
            
    # 4. Save the Output
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(base_dir, "outputs")
    output_file = os.path.join(output_dir, "signals_output.json")
    
    os.makedirs(output_dir, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(detected_signals, f, indent=4)
        
    logging.info(f"Complete! Found {len(detected_signals)} signals out of {len(raw_data)} posts.")
    logging.info(f"Results saved to: {output_file}")

if __name__ == "__main__":
    main()