# CHANGELOG.md

## [v0.0.3]

### Infrastructure
- **Safari CSS Download Management**:
  - Automatic download of external CSS files for Safari CORS compatibility  
  - Smart CI/GitHub Actions detection ensures assets are always present in deployment
  - Local development optimization: checks existing files, only downloads if missing
  - Environment variable `DOWNLOAD_SAFARI_CSS` for manual control
  - Improved error handling: critical failures stop CI deployment, warnings in local dev
  - Force download with `force_download=True` parameter in CI environments
  - Downloads Google Fonts, DaisyUI, KaTeX, and Papyrus styles locally
  - Documentation: `notes/SAFARI_CSS_DOWNLOAD.md`
  - Fixed: CI now skips CSS downloads entirely (files are committed to git)
  - Added: Better server startup retry logic in GitHub Actions build script
  - Safari CSS files are now committed to repository in `src/static/css/safari-local/`
  - 🔴 empty page at the end when printing... safari...

## [v0.0.2]

- Sujets0:
    - Safari:
        - svg working
        - text-2xs injection (TODO sel: generalize) 
        - button print multiple use if multiple generation / 🔴 empty page at the end when printing


[v0.0.1]

- Sujets0: 
    - Generation of pdf with 1 to 12 questions for 1 to 50 students
    - Working remotely using static website (except Fiches Réponses Enseignants)