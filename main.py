import datetime
from playwright.sync_api import sync_playwright
from dataclasses import dataclass, asdict, field
import pandas as pd
import argparse
import os
import sys

@dataclass
class Business:
    """holds business data"""
    name: str = None
    address: str = None
    domain: str = None
    website: str = None
    phone_number: str = None
    category: str = None
    location: str = None
    reviews_count: int = None
    reviews_average: float = None
    latitude: float = None
    longitude: float = None
    
    def __hash__(self):
        hash_fields = [self.name]
        if self.domain: hash_fields.append(f"domain:{self.domain}")
        if self.website: hash_fields.append(f"website:{self.website}")
        if self.phone_number: hash_fields.append(f"phone:{self.phone_number}")
        return hash(tuple(hash_fields))

@dataclass
class BusinessList:
    business_list: list[Business] = field(default_factory=list)
    _seen_businesses: set = field(default_factory=set, init=False)
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    save_at = os.path.join('GMaps Data', today)
    
    def __post_init__(self):
        os.makedirs(self.save_at, exist_ok=True)

    def add_business(self, business: Business):
        business_hash = hash(business)
        if business_hash not in self._seen_businesses:
            self.business_list.append(business)
            self._seen_businesses.add(business_hash)
    
    def dataframe(self):
        return pd.json_normalize((asdict(b) for b in self.business_list), sep="_")

    def save_to_excel(self, filename):
        self.dataframe().to_excel(f"{self.save_at}/{filename}.xlsx", index=False)

    def save_to_csv(self, filename):
        self.dataframe().to_csv(f"{self.save_at}/{filename}.csv", index=False)

def extract_coordinates_from_url(url: str) -> tuple[float, float]:
    try:
        coordinates = url.split('/@')[-1].split('/')[0]
        return float(coordinates.split(',')[0]), float(coordinates.split(',')[1])
    except:
        return 0.0, 0.0

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--search", type=str)
    parser.add_argument("-t", "--total", type=int)
    args = parser.parse_args()
    
    search_list = [args.search] if args.search else []
    if not search_list:
        input_path = os.path.join(os.getcwd(), 'input.txt')
        if os.path.exists(input_path):
            with open(input_path, 'r') as f:
                search_list = [line.strip() for line in f.readlines() if line.strip()]

    if not search_list:
        print('Error: Use -s or fill input.txt')
        sys.exit()

    total = args.total if args.total else 10

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False) # Keep False to solve CAPTCHAs
        context = browser.new_context(viewport={'width': 1280, 'height': 720})
        page = context.new_page()

        print("Navigating to Google Maps...")
        page.goto("https://www.google.com/maps", timeout=60000)
        
        # --- RESILIENT CONSENT BYPASS ---
        page.wait_for_timeout(2000)
        try:
            # Look for common "Accept" or "I agree" buttons
            for btn_text in ["Accept all", "Agree", "I agree", "Accept"]:
                btn = page.get_by_role("button", name=btn_text)
                if btn.count() > 0:
                    btn.click()
                    print(f"Clicked {btn_text} button.")
                    page.wait_for_timeout(2000)
                    break
        except: pass

        for search_for in search_list:
            print(f"Current search: {search_for}")
            
            # Use a broader selector for the search box
            search_box_selector = 'input.searchboxinput, #searchboxinput, [name="q"]'
            try:
                page.wait_for_selector(search_box_selector, timeout=60000)
                page.locator(search_box_selector).fill(search_for)
                page.keyboard.press("Enter")
            except Exception as e:
                print(f"Error: Could not find search box. Please check the browser window.")
                continue

            page.wait_for_timeout(5000)

            # Scrolling results
            previously_counted = 0
            while True:
                # Force hover on results list if possible
                try: page.hover('//a[contains(@href, "/maps/place/")]')
                except: pass
                
                page.mouse.wheel(0, 10000)
                page.wait_for_timeout(3000)
                
                current_count = page.locator('//a[contains(@href, "/maps/place/")]').count()
                print(f"Found {current_count} listings...", end='\r')
                
                if current_count >= total or current_count == previously_counted:
                    break
                previously_counted = current_count

            listings = page.locator('//a[contains(@href, "/maps/place/")]').all()[:total]
            business_list = BusinessList()

            for listing in listings:
                try:
                    listing.click()
                    page.wait_for_timeout(2500)

                    biz = Business()
                    # High-quality selectors
                    name_el = page.locator('h1.DUwDvf').first
                    biz.name = name_el.inner_text().strip() if name_el.count() > 0 else "Unknown"

                    # Data extraction
                    address_el = page.locator('button[data-item-id="address"]').first
                    biz.address = address_el.inner_text().strip() if address_el.count() > 0 else ""

                    web_el = page.locator('a[data-item-id="authority"]').first
                    biz.website = web_el.get_attribute('href') if web_el.count() > 0 else ""

                    phone_el = page.locator('button[data-tooltip="Copy phone number"]').first
                    biz.phone_number = phone_el.inner_text().strip() if phone_el.count() > 0 else ""

                    # Category/Location
                    biz.category = search_for.split(' in ')[0]
                    biz.location = search_for.split(' in ')[-1]
                    biz.latitude, biz.longitude = extract_coordinates_from_url(page.url)

                    business_list.add_business(biz)
                except Exception:
                    continue

            filename = search_for.replace(' ', '_')
            business_list.save_to_excel(filename)
            business_list.save_to_csv(filename)
            print(f"\nFinished scraping {search_for}")

        browser.close()

if __name__ == "__main__":
    main()