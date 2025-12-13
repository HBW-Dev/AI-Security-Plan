import requests
import sys
import pandas as pd
from lxml import html
from typing import List, Dict, Any


def fetch_and_save_quotes() -> None:
    """
    Fetches quotes form the target website, parse the HTML content.
    Cleans the data, and persists it to a CSV file.

    Target: http://quotes.toscrape.com/
    Output: quotes.csv
    """
    # Configuration
    # Define the target end point
    target_url = "http://quotes.toscrape.com/"

    # Configure real heads to mimic a real browser (Anti-Scraping measure)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    print(f"Initializing scrape to {target_url}")

    try:
        # Network request
        # Send a GET request with a strict timeout to prevent hanging
        response = requests.get(target_url, headers=headers, timeout=10)

        # Validate the response status code (Raise error if 4xx or 5xx)
        response.raise_for_status()

        # HTML Parsing
        # Convert the raw byte content into a structured Element Tree
        tree = html.fromstring(response.content)

        # Data Extraction Loop
        # We use a list to store data temporarily because appending to a lis is
        # much faster (O(1)) than appending to a Pandas DataFrame.
        data: List[Dict[str, str]] = []

        quote_elements = tree.xpath('//div[@class="quote"]')
        for quote in quote_elements:
            # Extract text content relative to the current quote element
            # Note: We use [0] assuming the structure is consistent
            text = quote.xpath('./span[@class="text"]/text()')[0]
            author = quote.xpath('.//small[@class="author"]/text()')[0]

            # Structure the data into a dictionary
            data_item = {"text": text, "author": author}
            data.append(data_item)

        print(f"Successfully extracted {len(data_item)} records.")

        # Data engineering (Pandas)
        # Create a DataFrame from the list of dictionaries
        df = pd.DataFrame(data)

        # Data cleaning: Strip whitespace from text fields to ensure data hygiene
        df["text"] = df["text"].str.strip()
        df["author"] = df["author"].str.strip()

        # Persistence (Save to Disk)
        # output_file = "quotes.csv"
        output_file = "quotes.xlsx"

        # Change to_csv -> to_excel
        # index=False: Hide the 0,1,2... row numbers
        # engine="openpyxl": Explicitly tell Pandas which tool to use
        # df.to_csv(output_file, index=False, encoding="utf-8-sig")
        df.to_excel(output_file, index=False, engine="openpyxl")

        print(f"Data pipeline complete. Output saved to: {output_file}")

        # Preview the first few rows for verification
        print("\n--- DataFrame Head Preview ---")
        print(df.head())

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Network Error: {e}")
        sys.exit(1)
    except IndexError as e:
        print(f"[ERROR] Parsing Error: (XPath failed): {e}")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] Unexpected Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    fetch_and_save_quotes()
