from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import simpleSplit


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