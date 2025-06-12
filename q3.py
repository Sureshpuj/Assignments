import requests
from bs4 import BeautifulSoup
import pandas as pd

# Set headers to mimic a browser
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                  " AppleWebKit/537.36 (KHTML, like Gecko)"
                  " Chrome/119.0.0.0 Safari/537.36"
}

# Function to scrape Flipkart
def scrape_flipkart(query):
    print("🔍 Searching Flipkart...")
    url = f"https://www.flipkart.com/search?q={query.replace(' ', '+')}"
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        results = []

        # Filter cards
        cards = soup.select("div._1AtVbE")

        for card in cards:
            name = card.select_one("div._4rR01T") or card.select_one("a.s1Q9rs")
            price = card.select_one("div._30jeq3")
            rating = card.select_one("div._3LWZlK")

            if name and price:
                results.append({
                    "Website": "Flipkart",
                    "Product Name": name.get_text(strip=True),
                    "Price": price.get_text(strip=True),
                    "Rating": rating.get_text(strip=True) if rating else "N/A"
                })
        return results
    except Exception as e:
        print(f" Error scraping Flipkart: {e}")
        return []

# Function to scrape Croma
def scrape_croma(query):
    print("🔍 Searching Croma...")
    url = f"https://www.croma.com/searchB?q={query.replace(' ', '%20')}"
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        results = []

        cards = soup.select("li.product-item")

        for card in cards:
            name = card.select_one("h3.product-title")
            price = card.select_one("span.new-price")
            rating = card.select_one("span.rating-count")

            if name and price:
                results.append({
                    "Website": "Croma",
                    "Product Name": name.get_text(strip=True),
                    "Price": price.get_text(strip=True),
                    "Rating": rating.get_text(strip=True) if rating else "N/A"
                })
        return results
    except Exception as e:
        print(f" Error scraping Croma: {e}")
        return []

# Combine and save results
def main():
    query = input("🔎 Enter product name to search: ").strip()
    if not query:
        print(" Product name cannot be empty.")
        return

    flipkart_data = scrape_flipkart(query)
    croma_data = scrape_croma(query)

    all_data = flipkart_data + croma_data

    if not all_data:
        print(" Product not found.")
        return

    df = pd.DataFrame(all_data)
    filename = f"{query.replace(' ', '_')}_products.xlsx"
    df.to_excel(filename, index=False)
    print(f" Saved {len(df)} products to {filename}")

if __name__ == "__main__":
    main()
