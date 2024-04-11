import requests
import json
from bs4 import BeautifulSoup

def scrape_data(company_code):
    #URL to be scraped
    url = f"https://www.screener.in/company/{company_code}/#quarters"
    #HTTP request to the URL
    response = requests.get(url)
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        #Find the table that is to be scraped
        table = soup.find('section', {'id': 'quarters'})
        #Extract the headers and rows from the table
        headers = [th.text.strip() for th in table.find('thead').find_all('th')]
        rows = table.find('tbody').find_all('tr')
        data = [dict(zip(headers, [td.text.strip() for td in row.find_all('td')])) for row in rows]
        #Convert the data to JSON format
        json_data = json.dumps(data, indent=2)
        print(json_data)
    else:
        print(f"Failed to load the URL. Status code: {response.status_code}")

scrape_data('vedl') #Enter the company code