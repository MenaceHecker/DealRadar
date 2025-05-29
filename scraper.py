import requests
from bs4 import BeautifulSoup

# --- CORRECTED TARGET URL ---
TARGET_URL = "https://www.amazon.com/Dell-G16-7630-Gaming-Laptop/dp/B0CKD892K1/"

def scrape_product_data(url):
    try:
        # --- Amazon often blocks requests without a proper User-Agent header ---
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            # You can find your current User-Agent by searching "what is my user agent" on Google.
        }

        # 1. Fetch the web page content
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)

        # 2. Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # --- 3. EXTRACT DATA FOR AMAZON LAPTOP PAGE ---
        #
        # Inspecting the Amazon page, typical elements for product name and price are:
        # Product Name: Element with id="productTitle"
        # Price: Elements like span class="a-price-whole" and span class="a-price-fraction"
        #        or span class="a-offscreen" (which holds the full price for screen readers)

        product_name_element = soup.find('span', id='productTitle')
        product_name = product_name_element.text.strip() if product_name_element else "Product Name Not Found"

        # Amazon's price structure can be tricky.
        # Often, the full price is stored in a hidden span for accessibility/screen readers.
        price_element = soup.find('span', class_='a-offscreen')
        product_price = price_element.text.strip() if price_element else "Price Not Found"

        # Fallback for price if a-offscreen isn't found (less reliable)
        if product_price == "Price Not Found":
            # Try to combine whole and fractional parts if available
            price_whole = soup.find('span', class_='a-price-whole')
            price_fraction = soup.find('span', class_='a-price-fraction')
            if price_whole and price_fraction:
                product_price = f"${price_whole.text.strip()}{price_fraction.text.strip()}"


        # Example of how you might get the current stock status
        # This will vary greatly by product and availability
        availability_element = soup.find('div', id='availability')
        availability = availability_element.text.strip() if availability_element else "Availability Not Found"


        return {
            "url": url,
            "product_name": product_name,
            "product_price": product_price,
            "availability": availability
        }

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err} for {url} (Status: {http_err.response.status_code})")
        print("This often means Amazon is blocking your request. Try rotating User-Agents or using proxies.")
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

if __name__ == "__main__": # Corrected 'if name' to 'if __name__'
    print(f"Attempting to scrape: {TARGET_URL}")
    data = scrape_product_data(TARGET_URL)
    if data:
        print("\n--- Scraped Data ---")
        for key, value in data.items():
            print(f"{key}: {value}")
    else:
        print("Failed to scrape data. Check for Amazon blocking or HTML structure changes.")

    print("\nNote: Amazon scraping can be inconsistent without advanced techniques like proxies or headless browsers.")
    print("If you encounter issues, try a simpler website first or consider using a dedicated web scraping API.")