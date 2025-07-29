from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_BREAK, WD_PARAGRAPH_ALIGNMENT
from docx.oxml import parse_xml
import re
import os

def create_two_column_docx(*texts, output_filename="multi_column_output.docx", 
                          font_name='Arial', font_size=11, column_spacing=0.5):
    """
    Create a two-column .docx file from multiple text inputs with automatic page breaks.
    Automatically formats section titles (Verse, Chorus, Bridge, Vamp) in bold with larger font.
    
    Args:
        *texts: Variable number of text strings to include
        output_filename (str): Name of the output .docx file
        font_name (str): Font name for the document
        font_size (int): Base font size for the document
        column_spacing (float): Space between columns in inches
    
    Returns:
        str: Path to the created file
    """
    if not texts:
        raise ValueError("At least one text argument must be provided")
    
    doc = Document()
    
    # Set default font for the document
    style = doc.styles['Normal']
    font = style.font
    font.name = font_name
    font.size = Pt(font_size)
    
    # Set up two-column layout
    section = doc.sections[0]
    setup_two_columns(section, column_spacing)
    
    # Process each text input
    for i, text in enumerate(texts):
        if i > 0:
            # Add a page break before each new text (except the first)
            add_page_break(doc)
        
        # Add the text content with formatting
        add_formatted_text_to_document(doc, text, font_name, font_size)
    
    # Save the document
    doc.save(output_filename)
    print(f"Multi-column document with {len(texts)} text sections saved as: {output_filename}")
    return output_filename

def create_continuous_two_column_docx(*texts, output_filename="lyrics.docx", 
                                     font_name='Arial', font_size=12, column_spacing=0.5, 
                                     separator_text="---"):
    """
    Create a two-column .docx file where all texts flow continuously with formatted titles.
    
    Args:
        *texts: Variable number of text strings to include
        output_filename (str): Name of the output .docx file
        font_name (str): Font name for the document
        font_size (int): Base font size for the document
        column_spacing (float): Space between columns in inches
        separator_text (str): Text to separate different input texts
    
    Returns:
        str: Path to the created file
    """
    if not texts:
        raise ValueError("At least one text argument must be provided")
    
    doc = Document()
    
    # Set default font
    style = doc.styles['Normal']
    font = style.font
    font.name = font_name
    font.size = Pt(font_size)
    
    # Set up two-column layout
    section = doc.sections[0]
    setup_two_columns(section, column_spacing)
    
    # Add all texts with separators
    for i, text in enumerate(texts):
        if i > 0 and separator_text:
            # Add separator between texts
            separator_para = doc.add_paragraph()
            separator_run = separator_para.add_run(separator_text)
            separator_run.font.name = font_name
            separator_run.font.size = Pt(font_size)
            separator_para.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
            doc.add_paragraph()  # Add some space
        
        # Add the text content with formatting
        add_formatted_text_to_document(doc, text, font_name, font_size)
        
        # Add space after each text section
        if i < len(texts) - 1:
            doc.add_paragraph()
    
    doc.save(output_filename)
    print(f"Continuous two-column document with {len(texts)} text sections saved as: {output_filename}")
    return output_filename

def add_formatted_text_to_document(doc, text, font_name, font_size):
    """
    Add text content to document with special formatting for section titles.
    Makes Verse, Chorus, Bridge, Vamp titles bold and 2 points larger.
    """
    if not text.strip():
        return
    
    # Split text into paragraphs
    paragraphs = text.split('\n\n') if '\n\n' in text else text.split('\n')
    
    for paragraph_text in paragraphs:
        if not paragraph_text.strip():
            continue
            
        # Check if this paragraph is a section title
        if is_section_title(paragraph_text.strip()):
            # Create paragraph for section title
            para = doc.add_paragraph()
            run = para.add_run(paragraph_text.strip())
            run.font.name = font_name
            run.font.size = Pt(font_size + 2)  # 2 points larger
            run.font.bold = True
        else:
            # Regular paragraph
            para = doc.add_paragraph()
            run = para.add_run(paragraph_text.strip())
            run.font.name = font_name
            run.font.size = Pt(font_size)

def is_section_title(text):
    """
    Check if a line of text is a section title (Verse, Chorus, Bridge, Vamp with optional numbers).
    Handles formats like: Verse, Verse1, Verse 1, Chorus, Chorus2, Bridge 3, etc.
    """
    # Pattern to match section titles with optional numbers and spacing
    pattern = r'^(Verse|Chorus|Pre-Chorus|Pre\s+Chorus|Bridge|Vamp)\s*\d*\s*:*$'
    return bool(re.match(pattern, text.strip(), re.IGNORECASE))

def setup_two_columns(section, column_spacing_inches=0.5):
    """Helper function to set up two-column layout for a section"""
    sectPr = section._sectPr
    # Remove existing column settings
    for cols in sectPr.xpath('./w:cols'):
        sectPr.remove(cols)
    
    # Convert inches to twips (1 inch = 1440 twips)
    space_twips = int(column_spacing_inches * 1440)
    
    # Add new column configuration
    cols_xml = f'<w:cols w:num="2" w:space="{space_twips}" xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"/>'
    cols = parse_xml(cols_xml)
    sectPr.append(cols)

def add_page_break(doc):
    """Helper function to add a page break"""
    para = doc.add_paragraph()
    run = para.add_run()
    run.add_break(WD_BREAK.PAGE)

def add_column_break(doc):
    """Helper function to add a column break"""
    para = doc.add_paragraph()
    run = para.add_run()
    run.add_break(WD_BREAK.COLUMN)

