# Simple Business Scraper

This is a small Python project. It tries to get basic public business info (name, address, maybe email, maybe website) for an Australian postcode from public directory pages. It uses requests and BeautifulSoup. It saves results to a JSON file.

The scrape can return few or even zero real businesses. Sites change often and can block scripts (403 or empty content). This code cant get through protected web. It is slow on purpose (delay between requests) so it does not spam a server.

## What it does
- Takes a postcode (4 digits)
- Tries to pull business name, address, email, website links it can see in the HTML
- Stores the list in `businesses_<postcode>.json`


## Requirements
- Python
- Packages in `requirements.txt` 

## Setup
Clone and enter the folder:
```
git clone https://github.com/michaelhardyy/Web-Scrapping.git
cd Web-Scrapping
```

Create a virtual environment:
```
python -m venv webs
./webs/Scripts/activate  (Windows PowerShell)
```

Install packages:
```
pip install -r requirements.txt
```

## Run
```
python scraper.py 3000
```


If it works you get a file like:
```
businesses_3000.json
```

## JSON example
```
[
  {
    "name": "Example Business",
    "address": "123 Street VIC 3000",
    "email": "N/A",
    "website": "N/A"
  }
]
```
