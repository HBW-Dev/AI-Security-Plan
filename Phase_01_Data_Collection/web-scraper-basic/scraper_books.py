import requests
import sys
from lxml import html


def fetch_books():
    """
    Fetches the page of books.toscrape.com/ using a fake User-Agent
    """

    target_url = "http://books.toscrape.com/"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    print(f"target_url: {target_url}")

    try:
        response = requests.get(target_url, headers=headers, timeout=10)
        response.raise_for_status()
        tree = html.fromstring(response.content)

        book_elements = tree.xpath('//article[@class="product_pod"]')
        print(f"[SUCCESS] Found {len(book_elements)} books in this page.\n")
        for book in book_elements:
            book_name = book.xpath("./h3/a/@title")[0]
            book_price = book.xpath('./div/p[@class="price_color"]/text()')[0]

            print(f"book: {book_name}")
            print(f"price: {book_price}\n")

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] {e}")
        sys.exit(1)
    except IndexError:
        print("[ERROR] Parsing error: Could not find excepted data.")
        sys.exit(1)


if __name__ == "__main__":
    fetch_books()
