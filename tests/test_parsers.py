import lyrics_parser
import txt_to_pdf
import url_parser


def test_strip_chords_from_lyrics_removes_chords_and_keeps_sections():
    raw_lyrics = """
Verse 1
G    D/F#   Em
Amazing grace how sweet the sound
**C** that saved a wretch like me
"""

    result = lyrics_parser.strip_chords_from_lyrics(raw_lyrics)

    assert "Verse 1" in result
    assert "Amazing grace how sweet the sound" in result
    assert "that saved a wretch like me" in result
    assert "D/F#" not in result
    assert "**C**" not in result


def test_append_title_prepends_song_name():
    result = lyrics_parser.append_title("Verse 1\nAmazing grace", "Amazing Grace")

    assert result == "Amazing Grace\nVerse 1\nAmazing grace"


def test_extract_song_title_from_url_formats_slug():
    url = "https://worshipchords.com/how-great-is-our-god-chords/"

    assert url_parser.extract_song_title_from_url(url) == "How Great Is Our God"


def test_get_content_type_from_url_extended_matches_supported_sites():
    assert url_parser.get_content_type_from_url_extended("https://pnwchords.com/song-name") == "tabcontent"
    assert url_parser.get_content_type_from_url_extended("https://example.com/song-name", default="fallback") == "fallback"


def test_pdf_helpers_map_fonts_escape_markup_and_match_sections():
    assert txt_to_pdf.get_pdf_font_pair("Times New Roman") == ("Times-Roman", "Times-Bold")
    assert txt_to_pdf.get_pdf_font_pair("Arial") == ("Helvetica", "Helvetica-Bold")
    assert txt_to_pdf.normalize_text_for_pdf("A & B < C > D") == "A &amp; B &lt; C &gt; D"
    assert txt_to_pdf.is_section_title("Chorus 2")
    assert not txt_to_pdf.is_section_title("Amazing Grace")
