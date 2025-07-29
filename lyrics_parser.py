import re

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