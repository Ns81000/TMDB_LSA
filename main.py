import requests
import configparser
import sys
import time

# --- Configuration ---
# These constants point to your configuration files.
CONFIG_FILE = 'config.ini'
TITLES_FILE = 'titles.txt'
API_VERSION = 3
API_BASE_URL = f"https://api.themoviedb.org/{API_VERSION}"

# --- Helper Functions ---

def load_config():
    """Loads API credentials from the config file."""
    config = configparser.ConfigParser()
    if not config.read(CONFIG_FILE):
        print(f"Error: Configuration file '{CONFIG_FILE}' not found.")
        print("Please create it with your TMDB API credentials.")
        sys.exit(1)
    try:
        return config['tmdb']
    except KeyError:
        print(f"Error: [tmdb] section not found in '{CONFIG_FILE}'.")
        sys.exit(1)

def get_headers(config):
    """Returns the authorization headers for authenticated API requests."""
    return {
        "accept": "application/json",
        "Authorization": f"Bearer {config['access_token']}"
    }

def search_media(title, config):
    """Searches for a movie or TV show by title using the /search/multi endpoint."""
    url = f"{API_BASE_URL}/search/multi"
    params = {"query": title, "api_key": config['api_key']}
    response = requests.get(url, params=params)
    response.raise_for_status()  # Will raise an exception for HTTP errors
    results = response.json().get('results', [])
    if results:
        # Prioritize movies and TV shows in results, filtering out people
        filtered_results = [r for r in results if r.get('media_type') in ['movie', 'tv']]
        if filtered_results:
            return filtered_results[0]
    return None

def get_existing_lists(config):
    """Fetches all lists for the configured account."""
    url = f"{API_BASE_URL}/account/{config['account_id']}/lists"
    headers = get_headers(config)
    params = {"api_key": config['api_key']}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json().get('results', [])

def create_new_list(config):
    """Creates a new list on TMDB and returns its ID."""
    list_name = input("Enter a name for your new list: ")
    list_description = input("Enter a description for the list: ")
    
    url = f"{API_BASE_URL}/list"
    headers = get_headers(config)
    params = {"api_key": config['api_key']}
    json_data = {
        "name": list_name,
        "description": list_description,
        "language": "en"
    }
    response = requests.post(url, headers=headers, params=params, json=json_data)
    response.raise_for_status()
    print(f"Successfully created list '{list_name}'.")
    # ** THE BUG FIX IS HERE **
    # The API response uses 'list_id', not 'id'.
    return response.json()['list_id']

def add_item_to_list(list_id, media_id, config):
    """Adds a media item to a specified list."""
    # First, check if the item is already in the list to avoid unnecessary errors
    if item_is_in_list(list_id, media_id, config):
        return "Already Exists"
        
    url = f"{API_BASE_URL}/list/{list_id}/add_item"
    headers = get_headers(config)
    params = {"api_key": config['api_key']}
    json_data = {"media_id": media_id}
    response = requests.post(url, headers=headers, params=params, json=json_data)
    
    # A 201 status code means the item was successfully added.
    if response.status_code == 201:
        return "Success"
    else:
        # If it fails for other reasons, raise the error to be caught in the main loop.
        response.raise_for_status()

def item_is_in_list(list_id, media_id, config):
    """Checks if a specific item is already present in a list."""
    url = f"{API_BASE_URL}/list/{list_id}/item_status"
    params = {"api_key": config['api_key'], "media_id": media_id}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get('item_present', False)
    return False

# --- Main Execution Block ---

def main():
    """Main script execution flow."""
    print("--- TMDB List Automator ---")
    
    try:
        config = load_config()
    except Exception as e:
        print(f"An error occurred loading the configuration: {e}")
        return

    # --- Step 1: Choose a TMDB List ---
    try:
        print("\nFetching your TMDB lists...")
        lists = get_existing_lists(config)
        if not lists:
            print("You have no existing lists. Let's create one.")
            list_id = create_new_list(config)
        else:
            print("Please choose a list to add titles to:")
            for i, lst in enumerate(lists):
                print(f"  {i + 1}: {lst['name']} ({lst['item_count']} items)")
            print("  0: Create a new list")

            choice = -1
            while choice < 0 or choice > len(lists):
                try:
                    choice = int(input("Enter your choice (number): "))
                except ValueError:
                    print("Invalid input. Please enter a number.")
            
            if choice == 0:
                list_id = create_new_list(config)
            else:
                list_id = lists[choice - 1]['id']
        
        print(f"\nSelected List ID: {list_id}")

    except requests.exceptions.HTTPError as e:
        print(f"\nError interacting with TMDB API: {e.response.status_code} - {e.response.text}")
        return
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return

    # --- Step 2: Read Titles from File ---
    try:
        with open(TITLES_FILE, 'r', encoding='utf-8') as f:
            titles = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"\nError: The input file '{TITLES_FILE}' was not found.")
        print("Please create it and add movie/TV show titles, one per line.")
        return

    print(f"\nFound {len(titles)} titles in '{TITLES_FILE}'. Starting process...\n")
    
    # --- Step 3: Process Each Title ---
    for title in titles:
        try:
            print(f"-> Searching for '{title}'...")
            media = search_media(title, config)
            
            if media:
                media_id = media['id']
                media_title = media.get('title') or media.get('name')
                media_type = media.get('media_type', 'N/A')
                print(f"   Found: '{media_title}' (Type: {media_type}, ID: {media_id})")
                
                status = add_item_to_list(list_id, media_id, config)
                
                if status == "Success":
                    print(f"   [SUCCESS] Added '{media_title}' to your list.\n")
                elif status == "Already Exists":
                    print(f"   [INFO] '{media_title}' is already in this list.\n")
                
            else:
                print(f"   [NOT FOUND] Could not find a match for '{title}'.\n")
            
            # Rate limiting to be respectful to the API (0.5 seconds between requests)
            time.sleep(0.5)

        except requests.exceptions.RequestException as e:
            print(f"   [ERROR] A network error occurred for '{title}': {e}\n")
        except Exception as e:
            print(f"   [ERROR] An unexpected error occurred for '{title}': {e}\n")

    print("--- Process Complete ---")


if __name__ == "__main__":
    main()