import json
import os
import logging
from utils.ingestion import scrape_dynamic_web
from signals.competitor_grievance import process_grievance_signal

# Set up logging for serverless environment
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def detect_signals(event, context):
    """
    AWS Lambda Handler function executed by the Serverless Framework.
    """
    logger.info("Serverless Invocation Started: Signal Detection Pipeline")
    
    # 1. Target URL
    sources = [
        {
            "name": "HackerNews Discussion (HackerRank)",
            "url": "https://news.ycombinator.com/item?id=31094484", 
            "item_selector": ".comtr",        
            "text_selector": ".commtext"      
        }
    ]
    
    raw_data = []
    
    # 2. Ingestion
    for source in sources:
        data = scrape_dynamic_web(
            url=source["url"], 
            source_name=source["name"],
            item_selector=source["item_selector"],
            text_selector=source["text_selector"]
        )
        raw_data.extend(data)
        
    if not raw_data:
        logger.error("Pipeline aborted: No data scraped.")
        return {"statusCode": 500, "body": json.dumps({"error": "No data scraped"})}
        
    detected_signals = []
    
    # 3. Processing
    logger.info("Analyzing text for competitor grievances...")
    for record in raw_data:
        signal = process_grievance_signal(record)
        if signal:
            detected_signals.append(signal)
            
    # 4. Output Generation (Writing to local file as per assignment constraints)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(base_dir, "outputs")
    output_file = os.path.join(output_dir, "signals_output.json")
    
    os.makedirs(output_dir, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(detected_signals, f, indent=4)
        
    logger.info(f"Pipeline complete. Detected {len(detected_signals)} valid signals.")
    
    # 5. Serverless HTTP Response Return
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": f"Success. {len(detected_signals)} signals detected.",
            "output_file": output_file,
            "signals": detected_signals
        })
    }