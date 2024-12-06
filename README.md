# Bukalapak Lazada Price Scraper

A Python library for scraping product prices from Bukalapak and Lazada.

## Installation

You can install the package from PyPI:

```python
pip install bukalapak-lazada-price-scrapper==0.1.0
```

## Requirements
- Selenium
- WebDriver Manager
- BeautifulSoup

## Usage

```python
from bukalapak_lazada_scraper import search

search_query = "iphone"

# Lazada
lazada_results = search('lazada', search_query)
print(lazada_results)

# Bukalapak
bukalapak_results = search('bukalapak', search_query)
print(bukalapak_results)
```

## Usage for other markeplace

it will automatic inject driver with beautifulsoap scraper and soap initilation

```python
from bukalapak_lazada_scraper import search

search_query = "iphone"

def some_marketplace_function(driver, init_soap, query):
  # code

result = search(some_marketplace_function, query)
print(result)
```

## Example of dynamic function

```python
def some_marketplace_function(driver, init_soap, query):
  # init
  url = f'https://url/?q={search_query}'

  driver.get(url)

  WebDriverWait(driver, 30).until(
    EC.presence_of_all_elements_located((By.CLASS_NAME, 'Ms6aG'))
  )

  page_source = driver.page_source

  soup = init_soup(page_source, 'html.parser')

  product_cards = soup.find_all('div', {'data-tracking': 'product-card'})

  for card in product_cards:
    name_tag = card.find('a', title=True)
    product_name = name_tag.text.strip() if name_tag else "No product name"

    price_tag = card.find('span', class_='ooOxS')
    product_price = price_tag.text.strip() if price_tag else "No price available"

    link_tag = card.find('a', href=True)
    product_link = f"https:{link_tag['href']}" if link_tag else "No link available"

    products.append({
        'name': product_name,
        'price': product_price,
        'link': product_link
    })

  # Sort products by price in ascending order (cheapest first)
  products.sort(key=lambda x: x['price'])

  return products
```
