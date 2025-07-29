from docx import Document
from docx.shared import Inches
from docx.enum.section import WD_SECTION
import os

def text_to_docx(text_content, output_filename, title=None):
    """
    Convert plain text to a .docx file
    
    Args:
        text_content (str): The text content to convert
        output_filename (str): Name of the output .docx file
        title (str, optional): Document title
    """
    # Create a new Document
    doc = Document()
    
    # Add title if provided
    if title:
        doc.add_heading(title, 0)
    
    # Split text into paragraphs (by double newlines or single newlines)
    paragraphs = text_content.split('\n\n') if '\n\n' in text_content else text_content.split('\n')
    
    # Add each paragraph to the document
    for paragraph in paragraphs:
        if paragraph.strip():  # Only add non-empty paragraphs
            doc.add_paragraph(paragraph.strip())
    
    # Save the document
    doc.save(output_filename)
    print(f"Document saved as: {output_filename}")


def advanced_text_to_docx(text_content, output_filename, title=None, font_name='Arial', font_size=15, columns=2):
    """
    Convert text to .docx with formatting options including column layout
    
    Args:
        text_content (str): The text content to convert
        output_filename (str): Name of the output .docx file
        title (str, optional): Document title
        font_name (str): Font name for the document
        font_size (int): Font size for the document
        columns (int): Number of columns (1 or 2)
    """
    from docx.shared import Pt
    from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
    
    doc = Document()
    
    # Set default font for the document
    style = doc.styles['Normal']
    font = style.font
    font.name = font_name
    font.size = Pt(font_size)
    
    # Add title if provided (title should be full width, not in columns)
    if title:
        heading = doc.add_heading(title, 0)
        heading.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    
    # Set up columns if requested
    if columns == 2:
        section = doc.sections[0]
        sectPr = section._sectPr
        cols = sectPr.xpath('./w:cols')[0] if sectPr.xpath('./w:cols') else None
        if cols is None:
            from docx.oxml import parse_xml
            cols_xml = '<w:cols w:num="2" w:space="720" xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"/>'
            cols = parse_xml(cols_xml)
            sectPr.append(cols)
    
    # Process text content
    paragraphs = text_content.split('\n\n') if '\n\n' in text_content else text_content.split('\n')
    
    for paragraph in paragraphs:
        if paragraph.strip():
            p = doc.add_paragraph(paragraph.strip())
    
    doc.save(output_filename)
    print(f"Formatted document saved as: {output_filename}")

def text_to_docx_two_columns(text_content, output_filename, title=None):
    """
    Convert plain text to a .docx file with two-column layout
    
    Args:
        text_content (str): The text content to convert
        output_filename (str): Name of the output .docx file
        title (str, optional): Document title
    """
    doc = Document()
    
    # Add title if provided (title spans full width)
    if title:
        doc.add_heading(title, 0)
    
    # Set up two-column layout
    section = doc.sections[0]
    sectPr = section._sectPr
    
    # Create column configuration XML
    from docx.oxml import parse_xml
    cols_xml = '<w:cols w:num="2" w:space="720" xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"/>'
    cols = parse_xml(cols_xml)
    sectPr.append(cols)
    
    # Split text into paragraphs
    paragraphs = text_content.split('\n\n') if '\n\n' in text_content else text_content.split('\n')
    
    # Add each paragraph to the document
    for paragraph in paragraphs:
        if paragraph.strip():
            doc.add_paragraph(paragraph.strip())
    
    # Save the document
    doc.save(output_filename)
    print(f"Two-column document saved as: {output_filename}")

def text_to_docx_with_column_break(left_column_text, right_column_text, output_filename, title=None):
    """
    Create a .docx file with specific content for left and right columns
    
    Args:
        left_column_text (str): Text for the left column
        right_column_text (str): Text for the right column
        output_filename (str): Name of the output .docx file
        title (str, optional): Document title
    """
    doc = Document()
    
    # Add title if provided
    if title:
        doc.add_heading(title, 0)
    
    # Set up two-column layout
    section = doc.sections[0]
    sectPr = section._sectPr
    
    from docx.oxml import parse_xml
    cols_xml = '<w:cols w:num="2" w:space="720" xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"/>'
    cols = parse_xml(cols_xml)
    sectPr.append(cols)
    
    # Add left column content
    left_paragraphs = left_column_text.split('\n\n') if '\n\n' in left_column_text else left_column_text.split('\n')
    for paragraph in left_paragraphs:
        if paragraph.strip():
            doc.add_paragraph(paragraph.strip())
    
    # Add column break
    from docx.enum.text import WD_BREAK
    p = doc.add_paragraph()
    run = p.runs[0] if p.runs else p.add_run()
    run.add_break(WD_BREAK.COLUMN)
    
    # Add right column content
    right_paragraphs = right_column_text.split('\n\n') if '\n\n' in right_column_text else right_column_text.split('\n')
    for paragraph in right_paragraphs:
        if paragraph.strip():
            doc.add_paragraph(paragraph.strip())
    
    doc.save(output_filename)
    print(f"Two-column document with specific content saved as: {output_filename}")