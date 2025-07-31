import re

def strip_chords_and_breaks(lyrics_text):
    """
    Strip chords and resulting line breaks from lyrics
    
    Args:
        lyrics_text (str): Raw lyrics with chords
        
    Returns:
        str: Clean lyrics without chords
    """
    lines = lyrics_text.strip().split('\n')
    clean_lines = []
    
    for line in lines:
        # Skip section headers (Intro, Verse 1, Chorus, etc.)
        if line.strip() and (line.strip().startswith(('Intro', 'Verse', 'Chorus', 'Pre-Chorus', 'Pre Chorus', 'Vamp', 'Refrain', 'Bridge', 'Outro')) 
                           or line.strip().replace(' ', '').replace('\t', '').isdigit()):
            clean_lines.append(line.strip())
            continue
        
        # Check if line contains only chords (letters, #, /, numbers, spaces)
        chord_pattern = r'^[A-G#/\d\s\-sus]+$'
        if re.match(chord_pattern, line.strip()) and line.strip():
            # This is likely a chord-only line, skip it
            continue
        
        # Process lines that contain both chords and lyrics
        # Remove chord annotations that appear above lyrics
        cleaned_line = line
        
        # Remove standalone chord symbols that are clearly chords
        chord_symbols = r'\b[A-G][#b]?(?:maj|min|m|sus[24]?|add[0-9]|[0-9])*(?:/[A-G][#b]?)?\b'
        
        # Split by spaces and filter out chord-like elements
        words = cleaned_line.split()
        lyric_words = []
        
        for word in words:
            # Skip if it's a pure chord symbol
            if re.match(r'^[A-G][#b]?(?:maj|min|m|sus[24]?|add[0-9]|[0-9])*(?:/[A-G][#b]?)?$', word):
                continue
            # Skip if it's just numbers or chord progression markers
            if re.match(r'^[\d\s\-]+$', word):
                continue
            lyric_words.append(word)
        
        # Reconstruct the line
        reconstructed = ' '.join(lyric_words).strip()
        
        # Only add non-empty lines that contain actual lyrics
        if reconstructed and not re.match(r'^[A-G#/\d\s\-sus]+$', reconstructed):
            clean_lines.append(reconstructed)
    
    # Join lines and clean up extra whitespace
    result = '\n'.join(clean_lines)
    
    # Remove multiple consecutive newlines
    result = re.sub(r'\n\s*\n\s*\n+', '\n\n', result)
    
    return result.strip()

def strip_chords_from_lyrics(lyrics_text):
    """
    More sophisticated chord stripping that handles inline chords better
    """
    lines = lyrics_text.strip().split('\n')
    clean_lines = []
    skip_next = False
    
    for i, line in enumerate(lines):
        if skip_next:
            skip_next = False
            continue
            
        line = line.strip()
        if not line:
            continue
        
        # Keep section headers
        if line.startswith(('Intro', 'Verse', 'Chorus', 'Pre-Chorus', 'Pre Chorus', 'Vamp', 'Refrain', 'Bridge', 'Outro')):
            clean_lines.append(line)
            continue
        
        # Check if this is a chord-only line
        chord_only_pattern = r'^[A-G#/\d\s\-sus]+$'
        if re.match(chord_only_pattern, line):
            continue
        
        # Check if next line exists and is lyrics that go with chord line
        if i + 1 < len(lines):
            next_line = lines[i + 1].strip()
            # If current line looks like chords and next line has lyrics
            if (re.match(chord_only_pattern, line) and next_line and 
                not re.match(chord_only_pattern, next_line) and
                not next_line.startswith(('Intro', 'Verse', 'Chorus', 'Pre-Chorus', 'Pre Chorus', 'Vamp', 'Refrain', 'Bridge', 'Outro'))):
                clean_lines.append(next_line)
                skip_next = True
                continue
        
        # Process mixed chord/lyric lines
        # Remove obvious chord symbols
        cleaned = re.sub(r'\b[A-G][#b]?(?:maj|min|m|sus[24]?|add[0-9]|[0-9])*(?:/[A-G][#b]?)?\b', '', line)
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        
        if cleaned and len(cleaned) > 2:  # Only keep substantial content
            clean_lines.append(cleaned)
    
    result = '\n'.join(clean_lines)
    result = re.sub(r'\n\s*\n\s*\n+', '\n\n', result)
    return result.strip()