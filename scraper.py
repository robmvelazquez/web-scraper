import requests
from bs4 import BeautifulSoup

def scrape_website(query, target_url):
    response = requests.get(target_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'lxml')
        print("Successfully fetched the website content")

        if query.lower() in soup.text.lower():
            print(f"Potential leak found on {target_url}")

        else:
            print(f"No leaks found for {query} on {target_url}")

        # Extract all links
        for link in soup.find_all('a'):
            print(link.get('href'))
    else:
        print(f"Failed to fetch the webpage. Status code: {response.status_code}")




if __name__ == "__main__":
    query = "digitalvixenx"
    target_url = "https://simpcity.su/threads/digitalvixenx-o-vixenafterhrs.33029/#post-5557027"
    scrape_website(query, target_url)
