import requests
import sys

def fetch_quotes():
    """
    Fetches the homepage of quotes.toscrape.com/ using a fake User-Agent.
    """

    # 1. Target URL
    # This is a famous sandbox for practicing scraping
    target_url = "http://quotes.toscrape.com/"

    # Disguise
    # We pretend to be chrome on Windows to avoid being blocked
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}
    
    print(f"Scraping {target_url}")

    try:
        # 3. Send Request
        response = requests.get(target_url, headers=headers, timeout=10)

        # 4. Check Success
        # raise_for_status() will throw an error if the status is 4xx or 5xx
        response.raise_for_status()

        # 5. Preview Content
        # Only print the first 500 character to keep the terminal clean
        print("\n--- Page Content (First 500 chars) ---")
        print(response.text[:500])
        print("\n... (truncated)")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    fetch_quotes()
        

