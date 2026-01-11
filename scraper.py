import requests
from bs4 import BeautifulSoup
import json

# List of URLs to check for sales
urls = [
    "https://warehouse.neweracap.com/collections/all-fitteds-sale",
    "https://www.hatclub.com/collections/fitted-sale-hats"
]

def scrape_hats():
    found_hats = []
    
    for url in urls:
        try:
            response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # This logic varies by site - this is a general example
            # It looks for common 'product' containers
            products = soup.select('.product-card') or soup.select('.grid-view-item')
            
            for p in products[:10]: # Get the top 10 from each site
                name = p.select_one('.product-card__title, .h4').text.strip()
                link = "https://warehouse.neweracap.com" + p.find('a')['href']
                img = p.find('img')['src']
                if img.startswith('//'): img = 'https:' + img
                
                found_hats.append({
                    "name": name,
                    "price": "Sale Item", # You can refine the price logic later
                    "orig": "Check Site",
                    "link": link,
                    "img": img
                })
        except Exception as e:
            print(f"Error scraping {url}: {e}")

    # Save to hats.json
    with open('hats.json', 'w') as f:
        json.dump(found_hats, f, indent=2)

if __name__ == "__main__":
    scrape_hats()
