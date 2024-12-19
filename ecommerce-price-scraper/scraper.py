# price_scraper/price_scraper/scraper.py

import os
import sys
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def check_chrome_installed():
    """ Check if Google Chrome is installed on the system. """
    try:
        if sys.platform == "win32":
            possible_paths = [
                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
            ]
            for path in possible_paths:
                if os.path.exists(path):
                    return True
            return False
        elif sys.platform == "darwin":
            return os.path.exists("/Applications/Google Chrome.app")
        elif sys.platform == "linux":
            return os.path.exists("/usr/bin/google-chrome")
        return False
    except Exception as e:
        print(f"Error checking Chrome installation: {e}")
        return False

def setup_driver():
    """ Setup the ChromeDriver with WebDriver Manager. """
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode (no UI)
    chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
    chrome_options.add_argument("--start-maximized")  # Maximize the browser window
    
    # Automatically download and use the correct ChromeDriver version
    driver_path = ChromeDriverManager().install()
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def get_bukalapak_product_prices(search_query):
    """ Scrape product prices from Bukalapak for a given search query. """
    if not check_chrome_installed():
        return {"error": "Google Chrome is not installed. Please install Chrome to continue."}

    # Construct the URL with the search query
    url = f'https://www.bukalapak.com/products?search[keywords]={search_query}'
    
    # Initialize the WebDriver
    driver = setup_driver()

    products = []

    try:
        # Open the Bukalapak search URL
        driver.get(url)

        # Wait for the price elements to be loaded
        WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'bl-product-card-new__price'))
        )

        # Get the page source after JS is rendered
        page_source = driver.page_source

        # Parse the page source with BeautifulSoup
        soup = BeautifulSoup(page_source, 'html.parser')

        # Find all product cards
        product_cards = soup.find_all('div', class_='bl-product-card-new__wrapper')

        if not product_cards:
            return {"error": "No product cards found. Page might not have loaded correctly."}

        # Extract product details
        for card in product_cards:
            # Extract product name
            name_tag = card.find('p', class_='bl-text bl-text--body-14 bl-text--secondary bl-text--ellipsis__2')
            product_name = name_tag.text.strip() if name_tag else "No product name"

            # Extract price
            price_tag = card.find('p', class_='bl-text bl-text--semi-bold bl-text--ellipsis__1 bl-product-card-new__price')
            product_price = price_tag.text.strip() if price_tag else "No price available"
            
            # Extract the product link
            link_tag = card.find('a', class_='bl-link')
            product_link = link_tag['href'] if link_tag else "No link available"

            # Store the product details as a dictionary
            products.append({
                'name': product_name,
                'price': product_price,
                'link': product_link
            })

        # Sort products by price in ascending order (cheapest first)
        products.sort(key=lambda x: x['price'])

        return products

    except Exception as e:
        return {"error": str(e)}
    finally:
        # Close the driver after scraping
        driver.quit()

def get_lazada_product_prices(search_query):
    """ Scrape product prices from Lazada for a given search query. """
    if not check_chrome_installed():
        return {"error": "Google Chrome is not installed. Please install Chrome to continue."}

    # Construct the URL with the search query for Lazada
    url = f'https://www.lazada.co.id/catalog/?q={search_query}'

    # Initialize the WebDriver
    driver = setup_driver()

    products = []

    try:
        # Open the Lazada search URL
        driver.get(url)

        # Wait for the price elements to be loaded
        WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'Ms6aG'))
        )

        # Get the page source after JS is rendered
        page_source = driver.page_source

        # Parse the page source with BeautifulSoup
        soup = BeautifulSoup(page_source, 'html.parser')

        # Find all product cards by using data-tracking="product-card"
        product_cards = soup.find_all('div', {'data-tracking': 'product-card'})

        if not product_cards:
            return {"error": "No product cards found. Page might not have loaded correctly."}

        # Extract product details
        for card in product_cards:
            # Extract product name
            name_tag = card.find('a', title=True)
            product_name = name_tag.text.strip() if name_tag else "No product name"

            # Extract price
            price_tag = card.find('span', class_='ooOxS')
            product_price = price_tag.text.strip() if price_tag else "No price available"

            # Extract the product link
            link_tag = card.find('a', href=True)
            product_link = f"https:{link_tag['href']}" if link_tag else "No link available"

            # Store the product details as a dictionary
            products.append({
                'name': product_name,
                'price': product_price,
                'link': product_link
            })

        # Sort products by price in ascending order (cheapest first)
        products.sort(key=lambda x: x['price'])

        return products

    except Exception as e:
        return {"error": str(e)}
    finally:
        # Close the driver after scraping
        driver.quit()

# Search wrapper function for easier usage
def lazada_search(query):
    """ A wrapper function for getting product prices by search query. """
    result = get_lazada_product_prices(query)
    if "error" in result:
        return result
    return json.dumps(result, indent=4)

def bukalapak_search(query):
    """ A wrapper function for getting product prices by search query. """
    result = get_bukalapak_product_prices(query)
    if "error" in result:
        return result
    return json.dumps(result, indent=4)

def search(function, query):
    """ A wrapper function for getting product prices by search query and platform. """
    
    # Case when 'function' is a string representing a platform name
    if isinstance(function, str):
        if function.lower() == "lazada":
            return lazada_search(query)
        elif function.lower() == "bukalapak":
            return bukalapak_search(query)
        else:
            return {"error": "Invalid platform. Please choose 'lazada' or 'bukalapak'."}
    
    # Case when 'function' is already a callable (a function)
    elif callable(function):
        if not check_chrome_installed():
            return {"error": "Google Chrome is not installed. Please install Chrome to continue."}
    
        driver = setup_driver()

        def init_soap(page_source):
            return BeautifulSoup(page_source, 'html.parser')

        # Call the function with the query and return the result
        return function(driver, init_soap, query)
    
    # If it's neither a string nor callable, return an error
    else:
        return {"error": "Invalid argument for 'function'. It should be a string or a callable."}