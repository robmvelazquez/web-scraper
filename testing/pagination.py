import requests

# Function to search Google Custom Search API for a target word with pagination
def google_search(query, api_key, cse_id, num_results=10, start_index=1):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'key': api_key,          # Your API Key
        'cx': cse_id,            # Custom Search Engine ID (cx)
        'q': query,              # Search query
        'num': num_results,      # Number of results to return (1-10)
        'start': start_index     # Start index for pagination (1, 11, 21, etc.)
    }
    
    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching results: {response.status_code}")
        return None

# Function to write search results to a file
def write_search_results(results, file_name='search_results.txt'):
    with open(file_name, 'a') as file:
        if "items" in results:
            for i, item in enumerate(results['items'], start=1):
                title = item['title']
                snippet = item.get('snippet', 'No description available')
                link = item['link']
                # Write the results to the file
                file.write(f"Title: {title}\n")
                file.write(f"Description: {snippet}\n")
                file.write(f"URL: {link}\n")
                file.write("\n")  # Newline for separation between results
        else:
            file.write("No search results found.\n")

# Start the program
if __name__ == "__main__":
    # Prompt the user for the target word
    target_word = input("Enter the word or content you want to search for: ")

# Replace with your Google API key and Custom Search Engine ID
    api_key = "AIzaSyDQMyqOxmS9xk-Urqnlugci_xbQZ2jmkic"
    cse_id = "77887bf79437a4026"
   
    # Define the total number of results you want (e.g., 30 results)
    total_results = 100
    results_per_page = 10  # Google Custom Search API allows max 10 results per request

    # Clear any previous content in the file
    open('search_results.txt', 'w').close()

    for start_index in range(1, total_results, results_per_page):
        print(f"Fetching results {start_index} to {start_index + results_per_page - 1}")
        
        # Perform the Google search with pagination
        results = google_search(target_word, api_key, cse_id, num_results=results_per_page, start_index=start_index)
        
        # Write the search results to a file
        if results:
            write_search_results(results)
    
    print(f"Results have been written to 'search_results.txt'.")











