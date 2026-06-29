@echo off
set /p search="Enter Search Term (e.g. Restaurants in Balmain): "
set /p total="Enter Total Leads to Scrape: "

echo Running Scraper...
.\venv\Scripts\python.exe main.py -s="%search%" -t=%total%

pause