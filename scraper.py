import requests
import json
from bs4 import BeautifulSoup

SCRAPERANT_API_KEY = '2407ab718734431687546f9de8597706'

# The updated list of stores with their specific sale pages
TARGET_STORES = [
    ("https://warehouse.neweracap.com/collections/all-fitteds-sale", "New Era Warehouse", "https://warehouse.neweracap.com"),
    ("https://www.hatclub.com/collections/fitted-sale-hats", "Hat Club", "https://www.hatclub.com"),
    ("https://capusa.nyc/collections/sale", "CapUSA", "https://capusa.nyc"),
    ("https://www.thelockerroomofdowney.com/collections/sale", "Locker Room Downey", "https://www.thelockerroomofdowney.com"),
    ("https://crownminded.com/collections/sale-fitteds", "Crown Minded", "https://crownminded.com"),
    ("https://606brims.com/collections/sale", "606 Brims", "https://606brims.com"),
    ("https://www.myfitteds.com/collections/sale", "MyFitteds", "https://www.myfitteds.com")
]

def scrape_hats():
    found_hats = []
    api_endpoint = "https://api.scrapingant.com/v2/general"

    for target_url, store_name, base_url in TARGET_STORES:
        params = {
            'url': target_url,
            'x-api-key': SCRAPERANT_API_KEY,
            'browser': 'true',
            'wait_for_selector': '.product-card, .product-item, .grid__item, .card-wrapper'
        }

        try:
            print(f"Scraping {store_name}...")
            response = requests.get(api_endpoint, params=params, timeout=60)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Shopify sites usually use one of these four container classes
                items = soup.select('.product-card, .product-item, .grid__item, .card-wrapper, .spb-item')
                
                print(f"Found {len(items)} possible items at {store_name}")

                for item in items[:20]:
                    try:
                        # Find Name - looks for titles or links with titles
                        name_tag = item.select_one('.product-card__title, .product-item__title, .card__heading, h3, h2')
                        if not name_tag: continue
                        name = name_tag.get_text(strip=True)
                        
                        # Find Link
                        link_tag = item.find('a', href=True)
                        if not link_tag: continue
                        raw_link = link_tag['href']
                        link = base_url + raw_link if raw_link.startswith('/') else raw_link
                        
                        # Find Image - handles standard and lazy-loading images
                        img_tag = item.find('img')
                        if not img_tag: continue
                        img_src = img_tag.get('data-src') or img_tag.get('srcset') or img_tag.get('src') or ""
                        
                        # Clean image URL
                        img = img_src.split(' ')[0].split('?')[0]
                        if img.startswith('//'): img = 'https:' + img

                        if name and link and img:
                            found_hats.append({
                                "name": f"[{store_name}] {name}",
                                "price": "SALE",
                                "orig": store_name,
                                "link": link,
                                "img": img
                            })
                    except:
                        continue
            else:
                print(f"Error at {store_name}: {response.status_code}")

        except Exception as e:
            print(f"System Error at {store_name}: {e}")

    # Save logic
    if len(found_hats) > 0:
        # Deduplicate based on link to avoid double entries
        unique_hats = {h['link']: h for h in found_hats}.values()
        with open('hats.json', 'w') as f:
            json.dump(list(unique_hats), f, indent=2)
        print(f"TOTAL: Saved
