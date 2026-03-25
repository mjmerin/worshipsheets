import asyncio
import os
from types import SimpleNamespace

import pytest

import main


@pytest.fixture(autouse=True)
def clear_temp_files():
    main.temp_files.clear()
    yield
    main.temp_files.clear()


def test_scrape_generates_docx_download(monkeypatch, tmp_path):
    generated = {}

    def fake_get(url, timeout):
        html = '<div class="song-chords-content">Verse 1\nAmazing grace</div>'
        return SimpleNamespace(text=html, raise_for_status=lambda: None)

    def fake_docx_generator(*texts, output_filename, font_name, font_size, column_spacing):
        generated["texts"] = texts
        generated["output_filename"] = output_filename
        generated["font_name"] = font_name
        generated["font_size"] = font_size
        generated["column_spacing"] = column_spacing
        with open(output_filename, "w", encoding="utf-8") as handle:
            handle.write("docx placeholder")

    monkeypatch.setattr(main.requests, "get", fake_get)
    monkeypatch.setattr(main.txt_to_docx, "create_continuous_two_column_docx", fake_docx_generator)
    monkeypatch.setattr(main.tempfile, "gettempdir", lambda: str(tmp_path))

    payload = asyncio.run(
        main.scrape_lyrics(
            urls=["https://worshipchords.com/amazing-grace-chords/"],
            filename="set_list",
            font_name="Arial",
            font_size=12,
            column_spacing=0.5,
            output_format="docx",
        )
    )

    assert payload["success"] is True
    assert payload["download_url"].startswith("/download/")
    assert generated["font_name"] == "Arial"
    assert generated["font_size"] == 12
    assert generated["column_spacing"] == 0.5
    assert generated["output_filename"].endswith(".docx")
    assert generated["texts"][0].startswith("Amazing Grace")


def test_scrape_generates_pdf_download_when_available(monkeypatch, tmp_path):
    generated = {}

    def fake_get(url, timeout):
        html = '<div class="song-chords-content">Verse 1\nAmazing grace</div>'
        return SimpleNamespace(text=html, raise_for_status=lambda: None)

    def fake_pdf_generator(*texts, output_filename, font_name, font_size, column_spacing):
        generated["texts"] = texts
        generated["output_filename"] = output_filename
        with open(output_filename, "w", encoding="utf-8") as handle:
            handle.write("pdf placeholder")

    fake_pdf_module = SimpleNamespace(create_continuous_two_column_pdf=fake_pdf_generator)

    monkeypatch.setattr(main.requests, "get", fake_get)
    monkeypatch.setattr(main, "txt_to_pdf", fake_pdf_module)
    monkeypatch.setattr(main.tempfile, "gettempdir", lambda: str(tmp_path))

    payload = asyncio.run(
        main.scrape_lyrics(
            urls=["https://worshipchords.com/amazing-grace-chords/"],
            filename="set_list",
            font_name="Arial",
            font_size=12,
            column_spacing=0.5,
            output_format="pdf",
        )
    )

    file_id = payload["download_url"].rsplit("/", 1)[-1]
    assert main.temp_files[file_id]["filename"] == "set_list.pdf"
    assert main.temp_files[file_id]["media_type"] == "application/pdf"
    assert generated["output_filename"].endswith(".pdf")


def test_scrape_rejects_invalid_output_format(monkeypatch):
    def fake_get(url, timeout):
        html = '<div class="song-chords-content">Verse 1\nAmazing grace</div>'
        return SimpleNamespace(text=html, raise_for_status=lambda: None)

    monkeypatch.setattr(main.requests, "get", fake_get)

    with pytest.raises(main.HTTPException) as error:
        asyncio.run(
            main.scrape_lyrics(
                urls=["https://worshipchords.com/amazing-grace-chords/"],
                filename="set_list",
                font_name="Arial",
                font_size=12,
                column_spacing=0.5,
                output_format="txt",
            )
        )

    assert error.value.status_code == 400
    assert error.value.detail == "Output format must be either docx or pdf"


def test_download_file_uses_stored_media_type(tmp_path):
    file_path = os.path.join(tmp_path, "lyrics.pdf")
    with open(file_path, "w", encoding="utf-8") as handle:
        handle.write("pdf placeholder")

    main.temp_files["file-123"] = {
        "path": file_path,
        "filename": "lyrics.pdf",
        "media_type": "application/pdf",
    }

    response = asyncio.run(main.download_file("file-123"))

    assert response.filename == "lyrics.pdf"
    assert response.media_type == "application/pdf"
