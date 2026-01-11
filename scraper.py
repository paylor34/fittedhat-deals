import requests
import json
from bs4 import BeautifulSoup

# Your API Key from the log
SCRAPERANT_API_KEY = '2407ab718734431687546f9de8597706'

def scrape_hats():
    found_hats = []
    
    # Define the ScrapingAnt endpoint and the target store
    api_endpoint = "https://api.scrapingant.com/v2/general"
    target_url = "https://warehouse.neweracap.com/collections/all-fitteds-sale"

    # We send the API key and URL as 'parameters' instead of one long string
    params = {
        'url': target_url,
        'x-api-key': SCRAPERANT_API_KEY,
        'browser': 'true'
    }

    try:
        print(f"Connecting to ScrapingAnt to reach: {target_url}")
        # Using 'params=' is safer and prevents typos in the URL
        response = requests.get(api_endpoint, params=params, timeout=60)
        
        print(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            items = soup.select('.product-card')
            print(f"Success! Found {len(items)} items.")

            for item in items[:20]:
                try:
                    name = item.select_one('.product-card__title').text.strip()
                    link_suffix = item.find('a', href=True)['href']
                    link = "https://warehouse.neweracap.com" + link_suffix
                    
                    img_tag = item.find('img')
                    img = "https:" + img_tag['src'].split('?')[0] if img_tag['src'].startswith('//') else img_tag['src']
                    
                    found_hats.append({
                        "name": name,
                        "price": "SALE",
                        "orig": "New Era Warehouse",
                        "link": link,
                        "img": img
                    })
                except:
                    continue
        else:
            print(f"API Error: {response.status_code} - {response.text}")

    except Exception as e:
        print(f"System Error: {e}")

    # Save results
    if len(found_hats) > 0:
        with open('hats.json', 'w') as f:
            json.dump(found_hats, f, indent=2)
        print(f"Saved {len(found_hats)} hats to hats.json")
    else:
        print("No hats found. Check if the 'product-card' class still exists on the site.")

if __name__ == "__main__":
    scrape_hats()
