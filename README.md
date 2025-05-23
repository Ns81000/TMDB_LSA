# TMDB List Automator

A Python utility to automatically create and populate lists on The Movie Database (TMDB) from a text file of titles.

![TMDB Logo](https://www.themoviedb.org/assets/2/v4/logos/v2/blue_square_2-d537fb228cf3ded904ef09b136fe3fec72548ebc1fea3fbbd1ad9e36364db38b.svg)

## 📋 Overview

The TMDB List Automator is a command-line tool that helps you:

- Create lists on your TMDB account
- Add multiple movies and TV shows to your lists by just providing their titles
- Search the TMDB database for accurate matches
- Skip duplicates automatically
- Process an entire text file of titles with a single command

Perfect for cinephiles and TV enthusiasts who want to quickly organize their watchlists, favorites, or thematic collections.

## 🛠️ Requirements

- Python 3.6 or higher
- `requests` library
- TMDB account and API credentials

## 🔧 Project Structure

```
TMDB/
│
├── main.py             # Main script to run the list automation
├── get_my_id.py        # Helper script to retrieve your TMDB account ID
├── config.ini          # Configuration file for API credentials
├── titles.txt          # Text file containing titles to be added to your list
└── readme.md           # This documentation
```

## ⚙️ Setup Instructions

### 1. Create a TMDB Account

If you don't already have one, create an account at [www.themoviedb.org](https://www.themoviedb.org/signup).

### 2. Get API Access

1. Go to your [TMDB account settings](https://www.themoviedb.org/settings/api)
2. Click on "API" in the left sidebar
3. Request an API key by filling out the form
4. Once approved, you'll receive:
   - API Key (v3 auth)
   - API Read Access Token

### 3. Get Your Account ID

Run the `get_my_id.py` script after replacing the placeholder with your API Read Access Token:

```python
# Edit this line in get_my_id.py:
access_token = "YOUR_ACCESS_TOKEN_HERE"
```

Then run:

```
python get_my_id.py
```

The script will display your TMDB account ID which you'll need for the next step.

### 4. Configure Your Credentials

Edit the `config.ini` file with your credentials:

```ini
[tmdb]
api_key = YOUR_API_KEY_HERE
access_token = YOUR_ACCESS_TOKEN_HERE
account_id = YOUR_ACCOUNT_ID_HERE
```

Replace the placeholders with your actual API key, access token, and account ID.

### 5. Prepare Your Title List

Create or edit `titles.txt` with movie and TV show titles, one per line. For example:

```
The Call
The Big Short
The Death of Stalin
The Wind Rises
Poacher
```

## 🚀 Usage

### Running the Tool

Simply execute the main script:

```
python main.py
```

### What Happens Next

1. The script will connect to TMDB using your credentials
2. It will display your existing lists or offer to create a new one
3. It will read all titles from `titles.txt`
4. For each title, it will:
   - Search the TMDB database
   - Find the best match (movie or TV show)
   - Add it to your selected list
   - Skip items that are already in the list
   - Report progress and any errors

## 🔄 Workflow Example

```
--- TMDB List Automator ---

Fetching your TMDB lists...
Please choose a list to add titles to:
  1: My Favorites (42 items)
  2: Watch Later (17 items)
  0: Create a new list

Enter your choice (number): 0
Enter a name for your new list: Best Thrillers
Enter a description for the list: A collection of the most suspenseful thrillers
Successfully created list 'Best Thrillers'.

Selected List ID: 8675309

Found 5 titles in 'titles.txt'. Starting process...

-> Searching for 'The Call'...
   Found: 'The Call' (Type: movie, ID: 159114)
   [SUCCESS] Added 'The Call' to your list.

-> Searching for 'The Big Short'...
   Found: 'The Big Short' (Type: movie, ID: 318846)
   [SUCCESS] Added 'The Big Short' to your list.

...

--- Process Complete ---
```

## 📝 Customization

### Adding More Titles

Simply edit the `titles.txt` file to add or remove titles. The script will process the entire file each time it runs.

### Rate Limiting

The script includes a 0.5-second delay between API requests to respect TMDB's rate limits. You can adjust this in the code if needed:

```python
# Line 192 in main.py - Increase if you encounter rate limit errors
time.sleep(0.5)
```

## ⚠️ Troubleshooting

### Common Issues

1. **"Configuration file not found"**
   - Make sure `config.ini` exists in the same directory as the script
   - Check that it has the correct format

2. **"[tmdb] section not found"**
   - Ensure your config.ini contains the [tmdb] section header

3. **API errors**
   - Verify your API credentials are correct
   - Check your internet connection
   - TMDB may be experiencing issues or maintenance

4. **"Title not found"**
   - Try using the full and exact title
   - Include the release year for movies with common titles (e.g., "The Fly 1986")

## 🛡️ Security Notes

- Never share your API key or access token
- Don't commit your `config.ini` file with real credentials to public repositories

## 📄 License

This project is released as open-source software. Feel free to modify and distribute it according to your needs.

## 🙏 Acknowledgments

- This tool uses the official [TMDB API](https://developers.themoviedb.org/3/getting-started/introduction)
- Icons and logos are property of TMDB

---

_Created with ❤️ for movie and TV enthusiasts_
