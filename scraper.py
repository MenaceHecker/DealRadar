import requests # Usually good for basic HTTP requests if needed, but less for main scraping
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time # For brief pauses if needed

# --- Target Amazon URL ---
TARGET_URL = "https://www.amazon.com/Google-Pixel-Unlocked-Smartphone-Advanced/dp/B0D7HWJDQM/ref=sr_1_4?crid=2IW5M3G8CZ9QY&dib=eyJ2IjoiMSJ9.9YRxo9HQbGPoJngmlwzUscX4tg4ju3yMjd1_9CKfyi9e6DubMOel5bYcC2pJYYTsjUD9TBBX1aURnLjy32V-pLWgjQzbOT3rm9DXYWc-Zqt9C0BGkBzGodtmz5n1CU2iQVq2yLZMnsq9l1SJwOkfaQhP5VOlpbCWcEdBMyIDK9mW_gpZAA6Df-xksSIfcvNbd6xqDX75tG0jGIU6NVFd8Loc0b-ENCHqOdKYKncH_Hc.3adOSx_GdwapwhemPokXFw1w1ZzNl-z92lELSm-baoM&dib_tag=se&keywords=Google%2BPixel&qid=1748532604&sprefix=google%2Bpixel%2B%2Caps%2C147&sr=8-4&th=1"
# --- Path to your ChromeDriver executable ---
# Make sure chromedriver is in the same directory as this script, or provide the full path.
CHROMEDRIVER_PATH = "./chromedriver.exe" # For Windows, use "./chromedriver" for Mac/Linux


def scrape_product_data_selenium(url):
    driver = None # Initialize driver to None
    try:
        # Set up Chrome options for headless mode
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--window-size=1920,1080") # Set a fixed window size
        chrome_options.add_argument("start-maximized")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled") # Hide automation control
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"]) # Remove "Chrome is being controlled by automated test software"
        chrome_options.add_experimental_option('useAutomationExtension', False) # Disable automation extension
        chrome_options.add_argument("--headless")   #Run Chrome in headless mode (no GUI)
        chrome_options.add_argument("--no-sandbox") # Required for some environments
        chrome_options.add_argument("--disable-dev-shm-usage") # Required for some environments
        # Optional: Add a more realistic User-Agent for headless browser
        chrome_options.add_argument(f"user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        # Optional: Disable images for faster loading (might break some layouts)
        # chrome_options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
        chrome_options.add_argument("--window-size=1920,1080") # Set a fixed window size


        # Initialize the WebDriver
        service = Service(executable_path=CHROMEDRIVER_PATH)
        driver = webdriver.Chrome(service=service, options=chrome_options)

        print(f"Opening URL with Selenium: {url}")
        driver.get(url)

        # --- IMPORTANT: Wait for specific elements to load ---
        # Instead of just time.sleep(), use WebDriverWait for robustness.
        # We wait until the product title (or price) element is present/visible.
        # You need to identify a reliable element that indicates the page is fully loaded.
        # For Amazon, 'productTitle' is usually one of the first.
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, 'productTitle'))
        )
        # You might add another wait for the price element if it loads separately:
        # WebDriverWait(driver, 10).until(
        #    EC.presence_of_element_located((By.CLASS_NAME, 'a-price-whole'))
        # )

        # Get the fully rendered page source
        page_source = driver.page_source

        # Now, use BeautifulSoup to parse the fully loaded HTML
        soup = BeautifulSoup(page_source, 'html.parser')

        # --- EXTRACT DATA FOR AMAZON LAPTOP PAGE ---
        # Use the same selectors as before, as they are often correct once loaded

        product_name_element = soup.find('span', id='productTitle')
        product_name = product_name_element.text.strip() if product_name_element else "Product Name Not Found"

        # Amazon's price structure can be tricky.
        # Often, the full price is stored in a hidden span for accessibility/screen readers.
        price_element = soup.find('span', class_='a-offscreen')
        product_price = price_element.text.strip() if price_element else "Price Not Found"

        # Fallback for price if a-offscreen isn't found (less reliable, but worth a try)
        if product_price == "Price Not Found":
            # Try to combine whole and fractional parts if available
            price_whole = soup.find('span', class_='a-price-whole')
            price_fraction = soup.find('span', class_='a-price-fraction')
            if price_whole and price_fraction:
                product_price = f"${price_whole.text.strip()}{price_fraction.text.strip()}"

        availability_element = soup.find('div', id='availability')
        availability = availability_element.text.strip() if availability_element else "Availability Not Found"


        return {
            "url": url,
            "product_name": product_name,
            "product_price": product_price,
            "availability": availability
        }

    except Exception as e:
        print(f"An error occurred during Selenium scraping: {e}")
        return None
    finally:
        # Ensure the browser is closed even if an error occurs
        if driver:
            driver.quit()


if __name__ == "__main__":
    print(f"Attempting to scrape: {TARGET_URL} using Selenium...")
    data = scrape_product_data_selenium(TARGET_URL) # Call the new Selenium function
    if data:
        print("\n--- Scraped Data ---")
        for key, value in data.items():
            print(f"{key}: {value}")
    else:
        print("Failed to scrape data. Check WebDriver path, Chrome version, or Amazon blocking.")

    print("\nNote: Even with Selenium, Amazon scraping is challenging and inconsistent.")
    print("You may still encounter CAPTCHAs or blocks. Consider proxies or scraping APIs for reliability.")
