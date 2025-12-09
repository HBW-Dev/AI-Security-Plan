import requests
import sys
from lxml import html # The Scalpel

def fetch_quotes():
    """
    Fetches the homepage of quotes.toscrape.com/ using a fake User-Agent.
    """

    # Target URL
    # This is a famous sandbox for practicing scraping
    target_url = "http://quotes.toscrape.com/"

    # Disguise
    # We pretend to be chrome on Windows to avoid being blocked
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    print(f"Scraping {target_url}")

    try:
        # Send Request
        response = requests.get(target_url, headers=headers, timeout=10)

        # Check Success
        # raise_for_status() will throw an error if the status is 4xx or 5xx
        response.raise_for_status()

        # Parse the HTML
        # tree is now a structured object, not just text
        tree = html.fromstring(response.content)
        print(f"tree: {tree}")

        # Find all quote containers
        # Xpath: //div[@class="quote"] means "Find any div with class='quote' " 
        quote_elements = tree.xpath('//div[@class="quote"]')
        print(f"quote_elements: {quote_elements}")

        print(f"[SUCCESS] Found {len(quote_elements)} quotes on this page. \n")

        # Extract details form each quote
        for quote in quote_elements:
            print(f"quote: {quote}")
            # Extract the title (The dot . means "current element")
            # We use [0] because xpath always return a list
            # safe to use ./ because it is a direct child
            text = quote.xpath('./span[@class="text"]/text()')[0]
            # MUST use .// because it is nested inside another <span>
            author = quote.xpath('.//small[@class="author"]/text()')[0]

            print(f"text {text}")
            print(f"author - {author}\n")

        # Preview Content
        # Only print the first 500 character to keep the terminal clean
        print("\n--- Page Content (First 500 chars) ---")
        print(response.text[:500])
        print("\n... (truncated)")
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Network Error: {e}")
        sys.exit(1)
    except IndexError:
        print(f"[ERROR] Parsing error: Could not find expected data.")
        sys.exit(1)

if __name__ == "__main__":
    fetch_quotes()
        

