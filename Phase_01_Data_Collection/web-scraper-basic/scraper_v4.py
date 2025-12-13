import requests
import sys
import pandas as pd
import time
import random
from lxml import html
from typing import List, Dict


def fetch_with_rotation(pages_to_scrape: int = 5):
    """
    Executes the 'Chameleon' scraping strategy to fetch quotes from multiple pages.

    This function iterates through the specified number of pages. For each quest,
    it rotates the User-Agent header and applies a random sleep delay to mimic
    human behavior and evade basic bot detection.

    The collected data is clean and persisted to 'quotes_chameleon.csv'

    :param pages_to_scrape: The number of pages to crawl, starting from page 1.
    :type pages_to_scrape: int
    """

    base_url = "http://quotes.toscrape.com/page/{}"

    # List of different browser identities
    user_agents = [
        # Chrome on Windows 10
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        # Firefox on Mac
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/115.0",
        # Safari on Mac
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
        # Edge on Windows
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
    ]

    all_quotes: List[Dict[str, str]] = []

    print(f"Starting Operation Chameleon: Target {pages_to_scrape} pages...")

    for page_num in range(1, pages_to_scrape + 1):
        # Select a Random Identity
        current_ua = random.choice(user_agents)

        headers = {"User-Agent": current_ua}

        # Random Delay (From previous lesson)
        delay = random.uniform(1, 3)
        if page_num > 1:
            print(f"Sleeping {delay:.2f}s...")
            time.sleep(delay)

        target_url = base_url.format(page_num)

        print(f"Page: {page_num} using: {current_ua[30]}...")

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

        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Network Error: {e}")
            sys.exit(1)
        except IndexError as e:
            print(f"[ERROR] Parsing Error (XPath failed): {e}")
            sys.exit(1)
        except Exception as e:
            print(f"[ERROR] Unexpected Error on page {page_num}: {e}")
            sys.exit(1)

    df = pd.DataFrame(all_quotes)

    raw_file = "quotes_raw_backup.csv"
    df.to_csv(raw_file, index=False, encoding="utf-8-sig")

    df["text"] = df["text"].str.strip()
    df["author"] = df["author"].str.strip()

    chameleon_file = "quotes_chameleon_clean.csv"
    df.to_csv(chameleon_file, index=False, encoding="utf-8-sig")

    print(
        f"\n[SUCCESS] Mission Complete. Scraped {len(df)} quotes across {pages_to_scrape} pages."
    )
    print(f"Saved to {raw_file}, {chameleon_file}")


if __name__ == "__main__":
    fetch_with_rotation()
