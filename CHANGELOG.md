# Changelog

## [1.0.2] - 2026-03-25

### Added
   - PDF export option for generated lyric sheets
   - Basic pytest coverage for parser helpers and export/download flows
   - GitHub Actions workflow to run tests on pushes and pull requests

### Changed
   - Allow users to choose between `.docx` and `.pdf` output formats in the web UI
   - Update download handling to return the correct filename and content type for each export format
   - Add ReportLab as a dependency for PDF generation
   - Preserve FastAPI `HTTPException` responses instead of converting validation errors into 500 errors

## [1.0.1] - 2026-01-19

### Added
   - Basic documentation

### Changed
   - Disable Google Adsense
   - Move configuration into a centralized `config.py` file.

## [1.0.0] - 2025-12-09

### Changed
   - Fixed login bug
   - Add versioning
   - Improved error messages
   - Complete move to Vercel from Render
   - Update README.md links