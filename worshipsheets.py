import requests
import sys
from bs4 import BeautifulSoup

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import simpleSplit

import re

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.platypus.doctemplate import PageTemplate, BaseDocTemplate, NextPageTemplate
from reportlab.platypus.frames import Frame
from reportlab.lib.colors import black

def create_two_column_pdf(text, filename, title=None):
    """
    Convert text to PDF with two-column layout using ReportLab
    """
    # Set up the document
    doc = BaseDocTemplate(filename, pagesize=letter)
    
    # Define frame dimensions
    page_width, page_height = letter
    margin = 0.75 * inch
    column_width = (page_width - 2 * margin - 0.25 * inch) / 2  # 0.25 inch gap between columns
    column_height = page_height - 2 * margin
    
    # Create frames for two columns
    left_frame = Frame(
        margin, margin, column_width, column_height,
        leftPadding=6, rightPadding=6, topPadding=6, bottomPadding=6
    )
    
    right_frame = Frame(
        margin + column_width + 0.25 * inch, margin, column_width, column_height,
        leftPadding=6, rightPadding=6, topPadding=6, bottomPadding=6
    )
    
    # Create page template with two columns
    two_column_template = PageTemplate(
        id='TwoColumn',
        frames=[left_frame, right_frame]
    )
    
    # Add template to document
    doc.addPageTemplates([two_column_template])
    
    # Get styles
    styles = getSampleStyleSheet()
    
    # Create custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=20,
        alignment=1,  # Center alignment
        textColor=black
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        spaceBefore=12,
        spaceAfter=8,
        textColor=black,
        keepWithNext=1
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=6,
        leading=12,
        textColor=black
    )
    
    # Build the story (content)
    story = []
    
    # Add title if provided (spans both columns)
    if title:
        story.append(Paragraph(title, title_style))
        story.append(Paragraph("<br/><br/>", body_style))
    
    # Process the text
    # Split by double newlines to identify paragraphs
    sections = text.split('\n\n')
    
    for section in sections:
        section = section.strip()
        if not section:
            continue
            
        lines = section.split('\n')
        
        # Check if first line might be a heading (shorter and title-case)
        if len(lines) > 1 and len(lines[0]) < 50 and lines[0].istitle():
            # Treat first line as heading
            story.append(Paragraph(lines[0], heading_style))
            # Rest as body text
            body_text = '\n'.join(lines[1:])
            if body_text.strip():
                # Replace single newlines with <br/> for line breaks within paragraphs
                formatted_text = body_text.replace('\n', '<br/>')
                story.append(Paragraph(formatted_text, body_style))
        else:
            # Treat entire section as body text
            formatted_text = section.replace('\n', '<br/>')
            story.append(Paragraph(formatted_text, body_style))
    
    # Build the PDF
    doc.build(story)
    print(f"Two-column PDF saved as {filename}")

def strip_chords_from_lyrics(lyrics):
    """
    Strip chord notations from lyrics text.
    This function removes:
    - Lines that contain only chord names and spaces
    - Chord names that appear at the beginning of lines
    - Chord names that appear inline with lyrics
    """
    lines = lyrics.split('\n')
    clean_lines = []
    
    # Pattern to match common chord notations
    chord_pattern = r'\b[A-G][#b]?(?:maj|min|m|sus|add|dim|aug|\d)*(?:/[A-G][#b]?)?\b'
    
    for line in lines:
        # Skip completely empty lines initially - we'll handle spacing later
        if not line.strip():
            clean_lines.append('')
            continue
            
        # Check if line contains only chords and whitespace
        # Remove all chord matches and see if anything meaningful remains
        line_without_chords = re.sub(chord_pattern, '', line)
        line_without_chords = re.sub(r'\s+', ' ', line_without_chords).strip()
        
        # If line is only chords (nothing left after removing chords), skip it
        if not line_without_chords:
            continue
            
        # For lines with both chords and lyrics, remove the chords
        # Handle chords at the beginning of lines (common format)
        clean_line = line
        
        # Remove chords that appear at the start of a line followed by lyrics
        clean_line = re.sub(r'^\s*' + chord_pattern + r'\s*', '', clean_line)
        
        # Remove chords that appear inline
        clean_line = re.sub(chord_pattern, '', clean_line)
        
        # Clean up extra whitespace
        clean_line = re.sub(r'\s+', ' ', clean_line).strip()
        
        # Only add the line if it has content after cleaning
        if clean_line:
            clean_lines.append(clean_line)
    
    # Join lines and clean up excessive blank lines
    result = '\n'.join(clean_lines)
    
    # Remove excessive blank lines (more than 2 consecutive)
    result = re.sub(r'\n\s*\n\s*\n+', '\n\n', result)
    
    return result.strip()

def text_to_pdf_reportlab(text, filename):
    """Convert text string to PDF using ReportLab"""
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    
    # Set margins
    margin = 50
    y_position = height - margin
    
    # Split text into lines that fit the page width
    lines = simpleSplit(text, 'Helvetica', 12, width - 2*margin)
    
    for line in lines:
        if y_position < margin:  # Start new page if needed
            c.showPage()
            y_position = height - margin
        
        c.drawString(margin, y_position, line)
        y_position -= 14  # Line spacing
    
    c.save()
    print(f"PDF saved as {filename}")

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
    stripped_text = strip_chords_from_lyrics(text)
    create_two_column_pdf(stripped_text, "test.pdf", "TEST")
    # text_to_pdf_reportlab(stripped_text, "test.pdf")
    
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





