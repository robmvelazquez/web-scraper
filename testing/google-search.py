import requests

# Function to search Google Custom Search API for a target word
def google_search(query, api_key, cse_id, num_results=10):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'key': api_key,          # Your API Key
        'cx': cse_id,            # Custom Search Engine ID (cx)
        'q': query,              # Search query
        'num': num_results       # Number of results to return (1-10)
    }
    
    response = requests.get(url, params=params)

    if response.status_code == 200:
        results = response.json()
        return results
    else:
        print(f"Error fetching results: {response.status_code}")
        return None

# Function to print search results
def print_search_results(results):
    if "items" in results:
        for i, item in enumerate(results['items'], start=1):
            title = item['title']
            snippet = item.get('snippet', 'No description available')
            link = item['link']
            print(f"Result {i}:")
            print(f"Title: {title}")
            print(f"Description: {snippet}")
            print(f"URL: {link}\n")
    else:
        print("No search results found.")

# Start the program
if __name__ == "__main__":
    # Prompt the user for the target word
    target_word = input("Enter the exact word or content you want to search for: ")

    # Modify the query to ensure exact match and exclude specific domains
    query = f'"{target_word}" -site:onlyfans.com -site:tiktok.com -site:twitch.tv -site:tracker.gg -site:youtube.com -site:linktr.ee -site:cash.app -site:threads.net -site:fansmetrics.com -site:twitter.com -site:fansly.com -site:sotwe.com -site:x.com'

    # Replace with your Google API key and Custom Search Engine ID
    api_key = "AIzaSyDQMyqOxmS9xk-Urqnlugci_xbQZ2jmkic"
    cse_id = "77887bf79437a4026"

    # Perform the Google search
    results = google_search(query, api_key, cse_id)

    # Print the search results
    if results:
        print_search_results(results)

