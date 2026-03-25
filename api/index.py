from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List
import requests
from bs4 import BeautifulSoup
import tempfile
import os
import uuid
from pathlib import Path

# Import your existing modules
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Import version info (optional - only if you add version.py)
try:
    from version import __version__
except ImportError:
    __version__ = "1.0.1"

import config
import lyrics_parser
import url_parser
import txt_to_docx
try:
    import txt_to_pdf
except ImportError:
    txt_to_pdf = None

app = FastAPI(
    title="WorshipSheets", 
    description="Clean chord symbols from worship lyrics",
    version=__version__
)

# Setup templates - Vercel needs absolute paths
BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Try to mount static files if directory exists
static_dir = BASE_DIR / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# Store temporary files
temp_files = {}

@app.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    """Serve the main webpage with AdSense configuration"""
    return templates.TemplateResponse("index.html", {
        "request": request,
        "show_ads": config.SHOW_ADS,
        "app_password": config.APP_PASSWORD,
        "adsense_client_id": config.ADSENSE_CLIENT_ID,
        "adsense_slots": config.ADSENSE_SLOTS
    })

@app.post("/scrape")
async def scrape_lyrics(
    urls: List[str] = Form(...),
    filename: str = Form("cleaned_lyrics"),
    font_name: str = Form("Arial"),
    font_size: int = Form(12),
    column_spacing: float = Form(0.5),
    output_format: str = Form("docx")
):
    """Process lyrics from multiple URLs and create a downloadable document"""
    if not urls or all(not url.strip() for url in urls):
        raise HTTPException(status_code=400, detail="Please provide at least one valid URL")
    
    text_list = []
    processed_songs = []
    errors = []
    
    for url in urls:
        url = url.strip()
        if not url:
            continue
            
        try:
            song_title = url_parser.extract_song_title_from_url(url)
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            content_type = url_parser.get_content_type_from_url_extended(url)

            if "pnwchords" in url:
                lyrics_header = soup.find('h2', class_='tabtitle', string='Lyrics')
                if lyrics_header:
                    content_div = lyrics_header.find_next_sibling('div', class_='tabcontent')
            else:
                content_div = soup.find('div', class_=content_type) 
            
            if content_div:
                text = content_div.get_text(separator='\n').strip()
                stripped_text = lyrics_parser.strip_chords_from_lyrics(text)
                stripped_text = lyrics_parser.append_title(stripped_text, song_title)
                text_list.append(stripped_text)
                processed_songs.append(song_title)
            else:
                errors.append(f"Could not find lyrics section for: {song_title} ({url})")
                
        except requests.RequestException as e:
            errors.append(f"Failed to fetch: {url} - {str(e)}")
        except Exception as e:
            errors.append(f"Error processing {url}: {str(e)}")
    
    if not text_list:
        error_msg = "No lyrics could be extracted from the provided URLs."
        if errors:
            error_msg += f" Errors: {'; '.join(errors)}"
        raise HTTPException(status_code=400, detail=error_msg)
    
    try:
        if font_size < 8 or font_size > 72:
            raise HTTPException(status_code=400, detail="Font size must be between 8 and 72 points")
        
        if column_spacing < 0.1 or column_spacing > 2.0:
            raise HTTPException(status_code=400, detail="Column spacing must be between 0.1 and 2.0 inches")
        
        safe_filename = "".join(c for c in filename if c.isalnum() or c in (' ', '-', '_')).rstrip()
        if not safe_filename:
            safe_filename = "cleaned_lyrics"

        output_format = output_format.lower()
        file_config = {
            "docx": {
                "extension": "docx",
                "media_type": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                "generator": txt_to_docx.create_continuous_two_column_docx,
            },
            "pdf": {
                "extension": "pdf",
                "media_type": "application/pdf",
                "generator": txt_to_pdf.create_continuous_two_column_pdf if txt_to_pdf else None,
            },
        }

        if output_format not in file_config:
            raise HTTPException(status_code=400, detail="Output format must be either docx or pdf")

        if output_format == "pdf" and not txt_to_pdf:
            raise HTTPException(status_code=500, detail="PDF export is unavailable because the PDF dependency is not installed")
        
        file_id = str(uuid.uuid4())
        selected_format = file_config[output_format]
        temp_filename = f"{safe_filename}_{file_id}.{selected_format['extension']}"
        temp_path = os.path.join(tempfile.gettempdir(), temp_filename)
        
        selected_format["generator"](
            *text_list,
            output_filename=temp_path,
            font_name=font_name,
            font_size=font_size,
            column_spacing=column_spacing
        )
        
        temp_files[file_id] = {
            'path': temp_path,
            'filename': f"{safe_filename}.{selected_format['extension']}",
            'media_type': selected_format['media_type']
        }
        
        message = f"Successfully processed {len(processed_songs)} song(s)"
        if errors:
            message += f". Some errors occurred: {'; '.join(errors[:3])}"
            if len(errors) > 3:
                message += f" and {len(errors) - 3} more."
        
        return {
            "success": True,
            "message": message,
            "download_url": f"/download/{file_id}",
            "processed_songs": processed_songs
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create document: {str(e)}")

@app.get("/download/{file_id}")
async def download_file(file_id: str):
    """Download the generated lyrics document"""
    if file_id not in temp_files:
        raise HTTPException(status_code=404, detail="File not found or expired")
    
    file_info = temp_files[file_id]
    file_path = file_info['path']
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File has been removed")
    
    return FileResponse(
        path=file_path,
        filename=file_info['filename'],
        media_type=file_info['media_type']
    )

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy", 
        "message": "Lyrics scraper is running",
        "version": __version__
    }

@app.get("/version")
async def version_info():
    """Get version information"""
    return {
        "version": __version__,
        "app_name": "WorshipSheets"
    }
