# Google Maps Scraper

A lightweight and customizable Google Maps scraping tool built with Python and Playwright. This project automates the extraction of business listings, contact information, ratings, addresses, and other publicly available metadata from Google Maps search results.

Designed for lead generation, market research, local SEO analysis, and business intelligence workflows.

> **Disclaimer:**
> This project is intended for educational and research purposes only. Users are responsible for complying with Google's Terms of Service and all applicable laws and regulations.

---

## Features

* Extract business names and categories
* Collect ratings and review counts
* Scrape phone numbers and websites
* Retrieve addresses and location details
* Export results to CSV and Excel formats
* Batch processing with multiple search queries
* Configurable result limits
* Built with Playwright for reliable browser automation

---

## Tech Stack

* Python
* Playwright
* Pandas
* OpenPyXL

---

## Project Structure

```bash
google-maps-scraper/
│
├── main.py
├── requirements.txt
├── input.txt
├── RunScraper.bat
├── README.md
├── .gitignore
└── GMaps Data/
```

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Tahir-Husnain/Google-Map-Scrapper.git
cd Google-Map-Scrapper
```

### 2. Create a Virtual Environment (Recommended)

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Playwright Browser

```bash
playwright install chromium
```

---

## Usage

### Single Search Query

```bash
python main.py -s="coffee shops in Seattle" -t=50
```

### Batch Search Queries

Add multiple search queries inside `input.txt`:

```txt
dentists in Boston, MA
plumbers in Austin, TX
restaurants in Chicago, IL
```

Run the scraper:

```bash
python main.py -t=30
```

---

## Output

The scraper automatically creates a dated folder inside:

```bash
GMaps Data/
```

Generated files include:

* CSV exports
* Excel spreadsheets
* Structured business listing data

Example output files:

```bash
coffee shops in Seattle.csv
coffee shops in Seattle.xlsx
```

Each record may include:

* Business Name
* Rating
* Review Count
* Phone Number
* Website
* Address
* Coordinates
* Categories
* Additional metadata

---

## Customization

You can easily customize the scraper to:

* Extract additional fields
* Modify scraping speed
* Change Playwright browser settings
* Enable headless or visible browser mode
* Add proxy support

Configuration can be adjusted directly inside the source files.

---

## Performance Notes

Google Maps may temporarily limit requests if scraping is too aggressive.

Recommended practices:

* Add delays between requests
* Use smaller location-based queries
* Avoid high-frequency scraping sessions
* Use proxies if necessary

---

## Example Use Cases

* Lead generation
* Local business research
* Competitor analysis
* SEO prospecting
* Market intelligence
* Agency outreach workflows

---

## Future Improvements

* Proxy rotation support
* Multithreaded scraping
* CAPTCHA handling
* GUI dashboard
* API integration
* AI-powered data enrichment

---

## License

This project is licensed under the MIT License.

---

## Author

Developed by Tahir Husnain
