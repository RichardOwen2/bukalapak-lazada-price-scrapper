# bukalapak.py

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

# Search wrapper function for easier usage
def search(query):
    """ A wrapper function for getting product prices by search query. """
    result = get_bukalapak_product_prices(query)
    if "error" in result:
        return result
    return json.dumps(result, indent=4)

# Example usage
if __name__ == "__main__":
    search_query = "iphone"
    result = search(search_query)
    print(result)