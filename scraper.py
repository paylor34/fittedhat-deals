import requests
import json

# PASTE YOUR API KEY HERE
SCRAPERANT_API_KEY = '2407ab718734431687546f9de8597706'

def scrape_hats():
    found_hats = []
    
    # The store URL we want to scrape
    target_url = "https://warehouse.neweracap.com/collections/all-fitteds-sale"
    
    # ScraperAnt API endpoint
    api_url = f"https://api.scraperant.com/v2/general?url={target_url}&x-api-key={SCRAPERANT_API_KEY}&browser=true"

    try:
        print("Requesting page via ScraperAnt...")
        response = requests.get(api_url, timeout=30)
        
        if response.status_code == 200:
            # ScraperAnt returns the HTML of the page
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Use the specific New Era Warehouse classes we found earlier
            items = soup.select('.product-card')
            print(f"Found {len(items)} product containers.")

            for item in items[:25]:
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
                except Exception as e:
                    continue
        else:
            print(f"ScraperAnt Error: {response.status_code} - {response.text}")

    except Exception as e:
        print(f"System Error: {e}")

    # Save results
    if len(found_hats) > 0:
        with open('hats.json', 'w') as f:
            json.dump(found_hats, f, indent=2)
        print(f"Successfully scraped {len(found_hats)} hats!")
    else:
        # Keep the existing hats.json if the scrape failed so the site doesn't go blank
        print("No hats found this run. Keeping old data.")

if __name__ == "__main__":
    scrape_hats()
