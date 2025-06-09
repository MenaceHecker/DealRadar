import requests
from bs4 import BeautifulSoup

# --- SAMPLE TARGET URL  ---
TARGET_URL = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"

def scrape_product_data(url):
    try:
        # User-Agent is less critical here
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        # 1. Fetch the web page content
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)

        # 2. Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # --- 3. EXTRACT DATA FOR TOSCRAPE.COM BOOK PAGE ---
        # (Based on inspecting this specific page's HTML)

        # Product Name 
        product_name_element = soup.find('h1') # This may or may not be the product name with an h1 tag 
        product_name = product_name_element.text.strip() if product_name_element else "Product Name Not Found"

        # Product Price 
        product_price_element = soup.find('p', class_='price_color')
        product_price = product_price_element.text.strip() if product_price_element else "Price Not Found"

        # Stock availability 
        availability_element = soup.find('p', class_='instock availability')
        availability = availability_element.text.strip() if availability_element else "Availability Not Found"


        return {
            "url": url,
            "product_name": product_name,
            "product_price": product_price,
            "availability": availability
        }

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err} for {url} (Status: {http_err.response.status_code})")
        return None
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err} for {url}")
        return None
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err} for {url}")
        return None
    except requests.exceptions.RequestException as req_err:
        print(f"An unexpected request error occurred: {req_err} for {url}")
        return None
    except Exception as e:
        print(f"An error occurred during parsing: {e}")
        return None

if __name__ == "__main__":
    print(f"Attempting to scrape: {TARGET_URL}")
    data = scrape_product_data(TARGET_URL)
    if data:
        print("\n--- Scraped Data ---")
        for key, value in data.items():
            print(f"{key}: {value}")
    else:
        print("Failed to scrape data.")

    print("\nNext steps: Explore other elements on books.toscrape.com or try a different simple static site!")
