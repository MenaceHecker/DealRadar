import requests
from bs4 import BeautifulSoup

# --- REPLACE THIS URL with the actual URL of the simple product page you chose ---
TARGET_URL = "https://www.example.com/some-product-page" # <--- IMPORTANT: Change this!

def scrape_product_data(url):
    try:
        # 1. Fetch the web page content
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)

        # 2. Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # --- 3. EXTRACT DATA (THIS IS THE PART YOU'LL CUSTOMIZE HEAVILY) ---
        #
        # This is where you'll use BeautifulSoup to find the specific elements
        # containing the product name and price.
        #
        # You'll need to inspect the HTML of your chosen website.
        # Right-click on the product name/price in your browser and select "Inspect" or "Inspect Element".
        # Look for common HTML tags like:
        #   - <h1>, <h2> for titles
        #   - <p>, <span> for text
        #   - <div> with specific classes/IDs
        #
        # Example (THIS WILL LIKELY NOT WORK FOR YOUR SITE, IT'S JUST AN EXAMPLE):
        product_name_element = soup.find('h1', class_='product-title')
        product_price_element = soup.find('span', class_='price')

        product_name = product_name_element.text.strip() if product_name_element else "Not Found"
        product_price = product_price_element.text.strip() if product_price_element else "Not Found"

        # --- END OF CUSTOMIZATION PART ---

        return {
            "url": url,
            "product_name": product_name,
            "product_price": product_price
        }

    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None
    except Exception as e:
        print(f"An error occurred during scraping: {e}")
        return None

if name == "main":
print(f"Attempting to scrape: {TARGET_URL}")
data = scrape_product_data(TARGET_URL)
if data:
print("\n--- Scraped Data ---")
for key, value in data.items():
print(f"{key}: {value}")
else:
print("Failed to scrape data.")

print("\nNext steps: Refine the 'EXTRACT DATA' section in scraper.py based on your target URL's HTML.")
print("Use your browser's 'Inspect Element' tool!")