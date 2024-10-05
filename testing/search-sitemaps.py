import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Function to search for a keyword in the sitemap
def search_sitemap_for_keyword(base_url, target_word):
    # Fetch the main sitemap
    sitemap_urls = fetch_sitemaps(base_url)
    
    if not sitemap_urls:
        print("No sitemaps found, exiting.")
        return

    # Search each sitemap for the target word
    for sitemap_url in sitemap_urls:
        search_in_sitemap(sitemap_url, target_word)

# Function to fetch multiple sitemaps (sitemap index)
def fetch_sitemaps(base_url):
    sitemap_url = urljoin(base_url, "/sitemap.xml")
    response = requests.get(sitemap_url)
    
    if response.status_code != 200:
        print(f"Failed to retrieve sitemap index from {sitemap_url}. Status code: {response.status_code}")
        return []

    sitemap_urls = []
    
    try:
        soup = BeautifulSoup(response.content, "xml")
        # Check if it's a sitemap index (contains <sitemap> elements pointing to other sitemaps)
        sitemaps = soup.find_all("sitemap")
        if sitemaps:
            # If it's a sitemap index, extract each individual sitemap URL
            for sitemap in sitemaps:
                loc = sitemap.find("loc").text
                sitemap_urls.append(loc)
            print(f"Found {len(sitemap_urls)} individual sitemaps.")
        else:
            # If it's a regular sitemap, return just this URL
            return [sitemap_url]
    
    except Exception as e:
        print(f"Error parsing sitemap index: {e}")
    
    return sitemap_urls

# Function to search the content of a sitemap for the target word
def search_in_sitemap(sitemap_url, target_word):
    response = requests.get(sitemap_url)
    
    if response.status_code != 200:
        print(f"Failed to retrieve sitemap from {sitemap_url}. Status code: {response.status_code}")
        return
    
    try:
        # Parse the sitemap XML
        soup = BeautifulSoup(response.content, "xml")
        urls_found = 0
        # Search for the target word in the <loc> tags or other text
        for loc in soup.find_all("loc"):
            loc_text = loc.text
            if target_word.lower() in loc_text.lower():
                print(f"Found '{target_word}' in URL: {loc_text}")
                urls_found += 1

        if urls_found == 0:
            print(f"No occurrences of '{target_word}' found in {sitemap_url}")
    
    except Exception as e:
        print(f"Error searching sitemap {sitemap_url}: {e}")

# Start the program
if __name__ == "__main__":
    base_url = "https://simpcity.su"  # Starting point (home page)
    
    # Prompt the user for the target word
    target_word = input("Enter the word or content you want to search for: ")

    # Start the search with the user-provided target word
    search_sitemap_for_keyword(base_url, target_word)
