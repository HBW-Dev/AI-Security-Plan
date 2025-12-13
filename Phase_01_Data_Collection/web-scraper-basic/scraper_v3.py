import requests
import sys
import pandas as pd
import time
import random
from lxml import html
from typing import List, Dict


def fetch_multiple_pages(pages_to_scrape: int = 5) -> None:
    """
    Scrapes multiple pages from quotes.toscrape.com with polite delays.

    :param pages_to_scrape: Description
    :type pages_to_scrape: int
    """

    base_url = "http://quotes.toscrape.com/page/{}/"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    all_quotes: List[Dict[str, str]] = []

    print(f"Starting Operation Ghost: Target {pages_to_scrape} pages...")

    # Loop through page 1 to 5
    for page_num in range(1, pages_to_scrape + 1):

        # THE SHIELD: Random Sleep (Politeness Strategy)
        # uniform(1, 3) generates a float like 1.234, 2.891
        # randint(1, 3) would generate integers 1, 2, 3 (Too robotic)
        delay = random.uniform(1, 3)

        if page_num > 1:
            print(f"Sleeping for {delay:.2f} seconds to look human...")
            time.sleep(delay)

        # Construct URL
        target_url = base_url.format(page_num)
        print(f"Scraping Page {page_num}: {target_url}")

        try:
            response = requests.get(target_url, headers=headers, timeout=10)
            response.raise_for_status()

            tree = html.fromstring(response.content)
            quote_elements = tree.xpath('//div[@class="quote"]')

            for quote in quote_elements:
                text = quote.xpath('./span[@class="text"]/text()')[0]
                author = quote.xpath('.//small[@class="author"]/text()')[0]

                row = {"text": text, "author": author, "page": page_num}
                all_quotes.append(row)

        except Exception as e:
            print(f"[ERROR] Error on page {page_num}: {e}")
            continue

    # Save Data
    df = pd.DataFrame(all_quotes)

    # Cleaning
    df["text"] = df["text"].str.strip()
    df["author"] = df["author"].str.strip()

    output_file = "quotes_multi_page.xlsx"
    df.to_excel(output_file, index=False, engine="openpyxl")

    print(
        f"\n[SUCCESS] Mission Complete. Scraped {len(df)} quotes across {pages_to_scrape} pages."
    )
    print(f"Saved to {output_file}")


if __name__ == "__main__":
    fetch_multiple_pages()
