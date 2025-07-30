import requests
import sys
from bs4 import BeautifulSoup

# local libraries
import lyrics_parser
import txt_to_pdf
import txt_to_docx

text_list = []

# URL of the song lyrics page
for arg in sys.argv[1:]:  # Slice the list to exclude sys.argv[0]
    url = arg

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
        text_queue.put(stripped_text)
        text_list.append(stripped_text)
    else:
        print(f"Could not find lyrics section on page: {url}.")

txt_to_docx.create_continuous_two_column_docx(*text_list)


