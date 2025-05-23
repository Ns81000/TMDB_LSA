import requests
import sys

# --- PASTE YOUR API READ ACCESS TOKEN HERE ---
# Get this from the TMDB website's API page
access_token = "YOUR_ACCESS_TOKEN_HERE"

# --- You don't need to change anything below this line ---

if "YOUR_ACCESS_TOKEN_HERE" in access_token:
    print("\nERROR: Please replace 'YOUR_ACCESS_TOKEN_HERE' with your actual token in the script.")
    sys.exit(1)

headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {access_token}"
}

print("\nContacting TMDB API...")

try:
    # This request uses Python's modern networking libraries
    response = requests.get("https://api.themoviedb.org/3/account", headers=headers, timeout=10)
    
    # This will check if the request was successful (e.g., status code 200)
    response.raise_for_status()  
    
    data = response.json()
    account_id = data.get("id")
    username = data.get("username")
    
    if account_id:
        print("\n✅ SUCCESS!")
        print(f"   Username: {username}")
        print(f"   Account ID: {account_id}")
        print("\nGreat! Please copy this Account ID and paste it into your config.ini file.")
    else:
        print("\n❌ ERROR: Connection was successful, but no 'id' was found in the response.")
        print("Response received:", data)

except requests.exceptions.RequestException as e:
    print("\n❌ AN ERROR OCCURRED:")
    print("This confirms a network or security issue is blocking Python.")
    print("Error details:", e)
    print("\nSuggestion: Are you on a work or school network? A firewall might be blocking the connection.")
