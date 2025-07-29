import requests
import sys
from bs4 import BeautifulSoup

import lyrics_parser
import txt_to_pdf

# URL of the song lyrics page
url = sys.argv[1]

# Send a GET request to the website
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find the main content div where lyrics are located
# content_div = soup.find('div', class_='tabcontent') #pnwchords
# content_div = soup.find('div', class_='page-wrap') #essentialworship
# content_div = soup.find('div', class_='ct-div-block') #colloborateworship
# content_div = soup.find('div', class_='lyrics-disp') #worshiptogether
content_div = soup.find('div', class_='song-chords-content') #worshipchords

# Extract and clean the text
if content_div:
    text = content_div.get_text(separator='\n').strip()
    stripped_text = lyrics_parser.strip_chords_from_lyrics(text)
    txt_to_pdf.create_two_column_pdf(stripped_text, "test.pdf", "TEST")
    
    # Find and extract the Lyrics
    lines = stripped_text.split('\n')
    lyrics_lines = []
    for line in lines:
            if line.strip() == "":
                break  # End of Verse 1
                lyrics_lines.append(line.strip())
    
    # Output the result
    for line in lines:
        print(line)
else:
    print("Could not find lyrics section on the page.")





