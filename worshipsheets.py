import requests
import sys
from bs4 import BeautifulSoup

# local libraries
import lyrics_parser
import title_parser
import txt_to_docx

text_list = []

# URL of the song lyrics page
for arg in sys.argv[1:]:  # Slice the list to exclude sys.argv[0]
    url = arg
    song_title = title_parser.extract_song_title_from_url(url)

    # Send a GET request to the website
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the main content div where lyrics are located
    content_div = soup.find('div', class_='song-chords-content') #worshipchords

    # Extract and clean the text
    if content_div:
        print(f"Extracting {song_title} lyrics from {url}.")
        text = content_div.get_text(separator='\n').strip()
        stripped_text = lyrics_parser.strip_chords_from_lyrics(text)
        stripped_text = lyrics_parser.append_title(stripped_text, song_title)
        text_list.append(stripped_text)
    else:
        print(f"Could not find lyrics section on page: {url}.")

txt_to_docx.create_continuous_two_column_docx(*text_list)


