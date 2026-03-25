import re

from reportlab.lib.colors import black
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.utils import simpleSplit
from reportlab.pdfgen import canvas
from reportlab.platypus import BaseDocTemplate, PageTemplate, Paragraph, Spacer
from reportlab.platypus.frames import Frame


def create_two_column_pdf(text, filename, title=None):
    """
    Convert text to PDF with two-column layout using ReportLab.
    """
    doc = BaseDocTemplate(filename, pagesize=letter)

    page_width, page_height = letter
    margin = 0.75 * inch
    column_width = (page_width - 2 * margin - 0.25 * inch) / 2
    column_height = page_height - 2 * margin

    left_frame = Frame(
        margin,
        margin,
        column_width,
        column_height,
        leftPadding=6,
        rightPadding=6,
        topPadding=6,
        bottomPadding=6,
    )
    right_frame = Frame(
        margin + column_width + 0.25 * inch,
        margin,
        column_width,
        column_height,
        leftPadding=6,
        rightPadding=6,
        topPadding=6,
        bottomPadding=6,
    )
    doc.addPageTemplates([PageTemplate(id="TwoColumn", frames=[left_frame, right_frame])])

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Heading1"],
        fontSize=16,
        spaceAfter=20,
        alignment=1,
        textColor=black,
    )
    heading_style = ParagraphStyle(
        "CustomHeading",
        parent=styles["Heading2"],
        fontSize=14,
        spaceBefore=12,
        spaceAfter=8,
        textColor=black,
        keepWithNext=1,
    )
    body_style = ParagraphStyle(
        "CustomBody",
        parent=styles["Normal"],
        fontSize=10,
        spaceAfter=6,
        leading=12,
        textColor=black,
    )

    story = []
    if title:
        story.append(Paragraph(normalize_text_for_pdf(title), title_style))
        story.append(Paragraph("<br/><br/>", body_style))

    for section in text.split("\n\n"):
        section = section.strip()
        if not section:
            continue

        lines = section.split("\n")
        if len(lines) > 1 and len(lines[0]) < 50 and lines[0].istitle():
            story.append(Paragraph(normalize_text_for_pdf(lines[0]), heading_style))
            body_text = "\n".join(lines[1:])
            if body_text.strip():
                story.append(Paragraph(normalize_text_for_pdf(body_text), body_style))
        else:
            story.append(Paragraph(normalize_text_for_pdf(section), body_style))

    doc.build(story)
    print(f"Two-column PDF saved as {filename}")
    return filename


def create_continuous_two_column_pdf(
    *texts,
    output_filename="lyrics.pdf",
    font_name="Arial",
    font_size=12,
    column_spacing=0.5,
    separator_text="\n",
):
    """
    Create a continuous two-column PDF with title and section formatting.
    """
    if not texts:
        raise ValueError("At least one text argument must be provided")

    base_font, bold_font = get_pdf_font_pair(font_name)
    doc = BaseDocTemplate(output_filename, pagesize=letter)

    page_width, page_height = letter
    margin = 0.5 * inch
    gutter = column_spacing * inch
    column_width = (page_width - (2 * margin) - gutter) / 2
    column_height = page_height - (2 * margin)

    left_frame = Frame(
        margin,
        margin,
        column_width,
        column_height,
        leftPadding=0,
        rightPadding=0,
        topPadding=0,
        bottomPadding=0,
    )
    right_frame = Frame(
        margin + column_width + gutter,
        margin,
        column_width,
        column_height,
        leftPadding=0,
        rightPadding=0,
        topPadding=0,
        bottomPadding=0,
    )
    doc.addPageTemplates([PageTemplate(id="TwoColumn", frames=[left_frame, right_frame])])

    styles = getSampleStyleSheet()
    normal_style = ParagraphStyle(
        "LyricsBody",
        parent=styles["Normal"],
        fontName=base_font,
        fontSize=font_size,
        leading=font_size + 2,
        spaceAfter=2,
        textColor=black,
    )
    first_line_style = ParagraphStyle(
        "LyricsTitle",
        parent=normal_style,
        fontName=bold_font,
        fontSize=font_size + 10,
        leading=font_size + 12,
        spaceAfter=6,
    )
    section_style = ParagraphStyle(
        "LyricsSection",
        parent=normal_style,
        fontName=bold_font,
        fontSize=font_size + 2,
        leading=font_size + 4,
        spaceAfter=3,
        spaceBefore=4,
    )
    separator_style = ParagraphStyle(
        "LyricsSeparator",
        parent=normal_style,
        alignment=1,
        spaceAfter=6,
    )

    story = []
    for index, text in enumerate(texts):
        if index > 0 and separator_text:
            separator_html = normalize_text_for_pdf(separator_text)
            if separator_html:
                story.append(Paragraph(separator_html, separator_style))
                story.append(Spacer(1, 0.08 * inch))

        first_line_processed = False
        for raw_line in text.split("\n"):
            line = raw_line.strip()
            if not line:
                story.append(Spacer(1, 0.08 * inch))
                continue

            line_html = normalize_text_for_pdf(line)
            if is_section_title(line):
                story.append(Paragraph(line_html, section_style))
            elif not first_line_processed:
                story.append(Paragraph(line_html, first_line_style))
                first_line_processed = True
            else:
                story.append(Paragraph(line_html, normal_style))

    doc.build(story)
    print(f"Continuous two-column PDF with {len(texts)} text sections saved as: {output_filename}")
    return output_filename


def get_pdf_font_pair(font_name):
    """
    Map UI font choices to built-in ReportLab fonts.
    """
    font_key = (font_name or "").strip().lower()
    font_map = {
        "arial": ("Helvetica", "Helvetica-Bold"),
        "helvetica": ("Helvetica", "Helvetica-Bold"),
        "verdana": ("Helvetica", "Helvetica-Bold"),
        "tahoma": ("Helvetica", "Helvetica-Bold"),
        "trebuchet ms": ("Helvetica", "Helvetica-Bold"),
        "calibri": ("Helvetica", "Helvetica-Bold"),
        "times new roman": ("Times-Roman", "Times-Bold"),
        "georgia": ("Times-Roman", "Times-Bold"),
    }
    return font_map.get(font_key, ("Helvetica", "Helvetica-Bold"))


def normalize_text_for_pdf(text):
    """
    Escape characters used by ReportLab paragraph markup while preserving line breaks.
    """
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace("\n", "<br/>")
    )


def is_section_title(text):
    """
    Check if a line of text is a common worship song section title.
    """
    pattern = r'^(\|)?(Verse|Chorus|Refrain|Pre-Chorus|Pre\s+Chorus|Bridge|Vamp)(\|)?\s*\d*\s*:*$'
    return bool(re.match(pattern, text.strip(), re.IGNORECASE))


def text_to_pdf_reportlab(text, filename):
    """
    Convert text string to a simple single-column PDF using ReportLab canvas.
    """
    pdf_canvas = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    margin = 50
    y_position = height - margin
    lines = simpleSplit(text, "Helvetica", 12, width - 2 * margin)

    for line in lines:
        if y_position < margin:
            pdf_canvas.showPage()
            y_position = height - margin

        pdf_canvas.drawString(margin, y_position, line)
        y_position -= 14

    pdf_canvas.save()
    print(f"PDF saved as {filename}")
    return filename
