import re
from urllib.parse import urlparse

def extract_song_title_from_url(url):
    """
    Extract and format song title from worship chords URL
    
    Args:
        url (str): URL like https://worshipchords.com/how-great-is-our-god-chords/
    
    Returns:
        str: Formatted song title like "How Great Is Our God"
    """
    try:
        # Parse the URL to get the path
        parsed_url = urlparse(url)
        path = parsed_url.path
        
        # Extract the slug (remove leading/trailing slashes and file extensions)
        slug = path.strip('/').split('/')[-1]
        
        # Remove common suffixes like -chords, -lyrics, -tabs, etc.
        slug = re.sub(r'-(chords|lyrics|tabs|guitar|piano|ukulele)$', '', slug, flags=re.IGNORECASE)
        
        # Replace hyphens with spaces
        title = slug.replace('-', ' ')
        
        # Convert to title case (capitalize each word)
        formatted_title = title.title()
        
        return formatted_title
        
    except Exception as e:
        return f"Error processing URL: {e}"
    
def get_content_type_from_url_extended(url, default='unknown'):
    """
    Extended version with more flexibility and a default return value.
    
    Args:
        url (str): The URL to analyze
        default (str): Default value to return if no pattern matches
        
    Returns:
        str: Content type identifier
    """
    # Convert to lowercase for case-insensitive matching
    url_lower = url.lower()
    
    # Define URL pattern mappings with priority order
    url_mappings = [
        ('worshipchords', 'song-chords-content'),
        ('pnwchords', 'tabcontent'),
        ('essentialworship', 'page-wrap'),
    ]
    
    # Check each pattern in order
    for pattern, content_type in url_mappings:
        if pattern in url_lower:
            return content_type
        
    return default