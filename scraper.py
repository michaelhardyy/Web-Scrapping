import requests
from bs4 import BeautifulSoup
import json
import sys

# Get postcode from command line
if len(sys.argv) != 2:
    print("Usage: python scraper.py <postcode>")
    sys.exit(1)

postcode = sys.argv[1]

# Check postcode is valid
if not postcode.isdigit() or len(postcode) != 4:
    print("Error: Postcode must be 4 digits")
    sys.exit(1)

print(f"Looking for businesses in postcode {postcode}...")

# Try different websites
websites = [
    f"https://www.yellowpages.com.au/search/listings?clue=&locationClue={postcode}",
    f"https://www.startlocal.com.au/businesses/{postcode}"
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

page = None
for url in websites:
    print(f"Trying: {url}")
    try:
        page = requests.get(url, headers=headers)
        print(f"Status: {page.status_code}")
        
        if page.status_code == 200:
            print("Success! Found a working website")
            break
        else:
            print("Website blocked or unavailable")
    except:
        print("Connection failed")

if page is None or page.status_code != 200:
    print("All websites blocked automated requests")
    sys.exit(1)

soup = BeautifulSoup(page.content, 'html.parser')

# Create empty list for businesses
all_businesses = []

# Find all business listings
businesses = soup.select('div.listing-item')
if not businesses:
    businesses = soup.select('div.search-result')
if not businesses:
    businesses = soup.select('article')

print(f"Found {len(businesses)} items on page")

# Extract data from each business
for business in businesses:
    # Get business name
    name_tag = business.select('a.listing-name')
    if not name_tag:
        name_tag = business.select('h3.listing-name')
    if not name_tag:
        name_tag = business.select('h2')
    if not name_tag:
        name_tag = business.select('h3')
    
    if name_tag:
        name = name_tag[0].text.strip()
    else:
        name = "N/A"
    
    # Skip navigation items
    skip_words = ['categories', 'popular', 'menu', 'search', 'browse', 'by category', 'by name']
    should_skip = False
    for word in skip_words:
        if word.lower() in name.lower():
            should_skip = True
            break
    
    if should_skip or len(name) < 4:
        continue
    
    # Get address
    address_tag = business.select('p.listing-address')
    if not address_tag:
        address_tag = business.select('span.address')
    if not address_tag:
        address_tag = business.select('p.address')
    
    if address_tag:
        address = address_tag[0].text.strip()
    else:
        address = "N/A"
    
    # Get email
    email_tag = business.select('a[href^="mailto:"]')
    if email_tag:
        email = email_tag[0].get('href').replace('mailto:', '')
    else:
        email = "N/A"
    
    # Get website
    website = "N/A"
    links = business.select('a[href^="http"]')
    for link in links:
        href = link.get('href')
        if 'yellowpages' not in href and 'mailto' not in href:
            website = href
            break
    
    # Add to list
    all_businesses.append({
        "name": name,
        "address": address,
        "email": email,
        "website": website
    })
    
    print(f"Found: {name}")

print(f"\nTotal businesses found: {len(all_businesses)}")

# Save to JSON file
filename = f'businesses_{postcode}.json'
with open(filename, 'w') as output_file:
    json.dump(all_businesses, output_file, indent=2)

print(f"Saved to {filename}")