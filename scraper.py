import requests
from bs4 import BeautifulSoup
import json

def scrape_hats():
    found_hats = []
    
    # We add a "User-Agent" to make the robot look like a Chrome browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    # 1. Scrape New Era Warehouse Sale
    try:
        url = "https://warehouse.neweracap.com/collections/all-fitteds-sale"
        print(f"Checking {url}...")
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # New Era Warehouse uses 'product-card' classes
        items = soup.select('.product-card')
        for item in items[:15]:
            name = item.select_one('.product-card__title').text.strip()
            # Find the link and make it full URL
            link_tag = item.find('a', href=True)
            link = "https://warehouse.neweracap.com" + link_tag['href']
            # Find the image
            img_tag = item.find('img')
            img = "https:" + img_tag['src'] if img_tag['src'].startswith('//') else img_tag['src']
            
            found_hats.append({
                "name": name,
                "price": "SALE", 
                "orig": "Discounted",
                "link": link,
                "img": img
            })
    except Exception as e:
        print(f"New Era Scrape Error: {e}")

    # 2. Scrape Hat Club Sale
    try:
        url = "https://www.hatclub.com/collections/fitted-sale-hats"
        print(f"Checking {url}...")
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # Hat Club uses different classes
        items = soup.select('.product-item') or soup.select('.product-card')
        for item in items[:15]:
            name_tag = item.select_one('.product-item__title, .product-card__title')
            if not name_tag: continue
            
            name = name_tag.text.strip()
            link_tag = item.find('a', href=True)
            link = "https://www.hatclub.com" + link_tag['href']
            img_tag = item.find('img')
            img = "https:" + img_tag['src'] if img_tag['src'].startswith('//') else img_tag['src']
            
            found_hats.append({
                "name": name,
                "price": "SALE",
                "orig": "Discounted",
                "link": link,
                "img": img
            })
    except Exception as e:
        print(f"Hat Club Scrape Error: {e}")

    # FINAL CHECK: If we found hats, save them. 
    # If we found NOTHING, don't overwrite with an empty file.
    if len(found_hats) > 0:
        with open('hats.json', 'w') as f:
            json.dump(found_hats, f, indent=2)
        print(f"Success! Saved {len(found_hats)} hats.")
    else:
        print("No hats found. Check site structure or block status.")

if __name__ == "__main__":
    scrape_hats()
