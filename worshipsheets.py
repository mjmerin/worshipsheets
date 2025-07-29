import requests
import sys
from bs4 import BeautifulSoup

# local libraries
import lyrics_parser
import txt_to_pdf
import txt_to_docx

# URL of the song lyrics page
url = sys.argv[1]

# Send a GET request to the website
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find the main content div where lyrics are located
content_div = soup.find('div', class_='song-chords-content') #worshipchords

# Extract and clean the text
if content_div:
    print(f"Extracting lyrics from {url}.")
    text = content_div.get_text(separator='\n').strip()
    stripped_text = lyrics_parser.strip_chords_from_lyrics(text)
    txt_to_docx.advanced_text_to_docx(stripped_text, "lyrics.docx", "Lyrics", columns=2) 
    
else:
    print(f"Could not find lyrics section on page: {url}.")





