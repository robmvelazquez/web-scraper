import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time

# A set to keep track of visited URLs
visited_urls = set()

# Function to crawl a website and search for content
def crawl_website(base_url, target_word, max_pages = 100000):
    # Queue of URLs to visit (Start with base URL)
    urls_to_visit = [base_url]
    base_domain = get_domain(base_url) # Extract the domain of the base URL

    while urls_to_visit and len(visited_urls) < max_pages:
        # Get the next URL to visit
        current_url = urls_to_visit.pop(0)

        # Make sure we don't visit the same URL twice
        if current_url in visited_urls:
            continue

        try:
            # Fetch the page content
            response = requests.get(current_url)
            visited_urls.add(current_url) # Mark the page as visited

            # Check if the request was successful
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, "lxml")
                print(f"Crawling {current_url}")


                # Search for the target word in the page content
                if target_word.lower() in soup.text.lower():
                    print(f"Found '{target_word}' on {current_url}")

                # Extract all internal links and add them to the queue
                for link in soup.find_all('a', href=True):
                    href = link.get('href')
                    # Convert relative URLs to absolute URLs
                    full_url = urljoin(base_url, href)

                    #Only follow internal links (same domain)
                    if is_internal_link(full_url, base_domain) and full_url not in visited_urls:
                        urls_to_visit.append(full_url)

            time.sleep(1) # Avoid making requests too quickly (politeness)
        except Exception as e:
            print(f"Error while crawling {current_url}: {e}")

    print(f"Crawling complete. Visited {len(visited_urls)} pages.")

# Function to check if a link is internal (within the same domain)
def is_internal_link(full_url, base_domain):
    full_domain = get_domain(full_url)
    return base_domain == full_domain

# Helper function to extract the domain from a URL
def get_domain(url):
    return urlparse(url).netloc

# Start crawling
if __name__ == "__main__":
    base_url = "https://simpcity.su" # Starting point (home page)
    target_word = "digitalvixenx"
    crawl_website(base_url, target_word)

