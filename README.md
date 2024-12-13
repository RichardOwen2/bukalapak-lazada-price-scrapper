# Bukalapak Lazada Price Scraper

A Python library for scraping product prices from Bukalapak and Lazada.

## Installation

You can install the package from PyPI:

```python
pip install bukalapak-lazada-price-scrapper
```

## Requirements
- Selenium
- WebDriver Manager
- BeautifulSoup

## Usage

```python
from bukalapak_lazada_price_scrapper import search

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
from bukalapak_lazada_price_scrapper import search

search_query = "iphone"

def some_marketplace_function(driver, init_soap, query):
  # code

result = search(some_marketplace_function, query)
print(result)
```

## Example of dynamic function

```python
def some_marketplace_function(driver, init_soup, query):
  url = f'https://www.bukalapak.com/products?search[keywords]={search_query}'

  try:
    # Open the Marketplace url
    driver.get(url)

    # Wait for the price elements to be loaded
    WebDriverWait(driver, 30).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'bl-product-card-new__price'))
    )

    # Get the page source after JS is rendered
    page_source = driver.page_source

    # Initialize Beautiful soup
    soup = init_soup(page_source, 'html.parser')

    # Search Product Logic
    product_cards = soup.find_all('div', class_='bl-product-card-new__wrapper')

    if not product_cards:
        return {"error": "No product cards found. Page might not have loaded correctly."}

    for card in product_cards:
        name_tag = card.find('p', class_='bl-text bl-text--body-14 bl-text--secondary bl-text--ellipsis__2')
        product_name = name_tag.text.strip() if name_tag else "No product name"

        price_tag = card.find('p', class_='bl-text bl-text--semi-bold bl-text--ellipsis__1 bl-product-card-new__price')
        product_price = price_tag.text.strip() if price_tag else "No price available"
        
        link_tag = card.find('a', class_='bl-link')
        product_link = link_tag['href'] if link_tag else "No link available"

        products.append({
            'name': product_name,
            'price': product_price,
            'link': product_link
        })

    products.sort(key=lambda x: x['price'])

    return products
  except Exception as e:
      return {"error": str(e)}
  finally:
      driver.quit()
```
