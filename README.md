# Vikaas.ai Signal Detection System

A robust, serverless-ready Python data pipeline designed to ingest dynamic web content, extract competitor grievance signals using rule-based Natural Language Processing (NLP), and output structured machine-readable intelligence.

## 🚀 Overview

This system identifies potential hiring-related business signals (specifically negative feedback regarding competitor tools like HackerRank, HireVue, and Codility) from public web sources. It processes raw text through a multi-stage ETL (Extract, Transform, Load) pipeline to generate contextual insights for Vikaas.ai's outreach platforms.

**Key Features:**
* Pure Python 3 implementation (No LLMs or external AI APIs).
* Dynamic web scraping utilizing headless Chromium browsers.
* Robust rule-based text analysis using compiled Regular Expressions.
* Modular, serverless-friendly architecture.

---

## 🛠️ Setup and Execution

### Prerequisites
* Python 3.8 or higher
* `pip` package manager

### Installation
1. **Clone the repository:**
   ```bash
   git clone <your-repository-url>
   cd signal_detector# signal_detector

  Install dependencies:
The project utilizes Playwright to handle dynamic, JavaScript-rendered web scraping.

Bash
pip install -r requirements.txt
Install Browser Binaries:
Download the required Chromium binary for the headless scraper.

Bash
playwright install chromium
Running the Pipeline
Execute the main orchestrator script from the root directory:

Bash
python main.py
Viewing Results
Upon successful execution, the structured intelligence will be saved to:
outputs/signals_output.json

🏗️ Design & Architecture Explanation
The system is separated into highly modular components, ensuring that ingestion methods, scoring mathematics, and business rules can be updated independently.

1. Data Ingestion Approach (utils/ingestion.py)
Modern review sites and forums heavily rely on client-side JavaScript rendering, which causes standard HTTP requests (like urllib or requests) to fail.

Solution: I implemented Playwright via its synchronous API. This allows the system to launch a headless browser, emulate a standard user-agent, wait for the DOM to fully load (domcontentloaded), and precisely extract text using targeted CSS selectors.

Serverless Deployment: To deploy this specific Playwright ingestion module in a serverless environment (e.g., AWS Lambda, Google Cloud Run), the application should be packaged inside a Docker container (via AWS ECR or Google Artifact Registry) to accommodate the Chromium browser binaries.

2. Signal Detection & Scoring Logic (signals/competitor_grievance.py)
To strictly adhere to the "no LLMs" constraint, the transformation engine relies on highly optimized Rule-Based NLP.

Regex Engine: Target keywords and competitor names are mapped to specific business pain points (e.g., "expensive" maps to "Cost"). These keywords are evaluated using pre-compiled Regular Expressions.

Edge Case Handling: The regex utilizes word boundary limiters (\b). This ensures exact-word matching, preventing partial-match false positives (e.g., matching the grievance "bias" without falsely triggering on the word "biasing").

Scoring (utils/scoring.py): The system uses a weighted deterministic model. It assigns a base confidence score of 40 for identifying a competitor within the text, and adds a +20 weight for every distinct negative pain point identified, capped at a maximum score of 100.

3. Assumptions and Limitations
Contextual Negation: As a purely rule-based system without neural network inference, it lacks contextual nuance. For example, a text block stating "HireVue is NOT expensive" will trigger a false-positive signal because both target keywords exist within the exact string.

Target Selectors: The web scraper relies on specific HTML/CSS structures (e.g., .commtext on HackerNews). If the target website updates its DOM structure, the selectors in main.py must be updated.
