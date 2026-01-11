import requests
from bs4 import BeautifulSoup
import json

def scrape_hats():
    found_hats = []
    
    # We use a very common browser header
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'
    }

    # Sites to try
    # We will try the Warehouse site first as it is usually more open
    url = "https://warehouse.neweracap.com/collections/all-fitteds-sale"
    
    try:
        print(f"Attempting to read: {url}")
        session = requests.Session()
        res = session.get(url, headers=headers, timeout=15)
        
        print(f"Response Code: {res.status_code}")
        
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, 'html.parser')
            # Look for ANY link that contains "products" to see if we got the page
            items = soup.find_all('div', class_='product-card')
            
            for item in items[:20]:
                try:
                    name = item.find('div', class_='product-card__title').text.strip()
                    link = "https://warehouse.neweracap.com" + item.find('a')['href']
                    img = "https:" + item.find('img')['src'].split('?')[0] # Clean image URL
                    
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
            print(f"Blocked by site. Status: {res.status_code}")

    except Exception as e:
        print(f"Error: {e}")

    # If we found data, save it!
    if len(found_hats) > 0:
        with open('hats.json', 'w') as f:
            json.dump(found_hats, f, indent=2)
        print(f"Successfully saved {len(found_hats)} hats!")
    else:
        # If blocked, we put one "Error Hat" so you know the script ran but failed
        error_data = [{
            "name": "Bot Blocked - Trying to bypass...",
            "price": "N/A",
            "orig": "N/A",
            "link": "#",
            "img": "https://via.placeholder.com/150?text=Blocked+By+Store"
        }]
        with open('hats.json', 'w') as f:
            json.dump(error_data, f, indent=2)
        print("No hats found - check logs for block message.")

if __name__ == "__main__":
    scrape_hats()
