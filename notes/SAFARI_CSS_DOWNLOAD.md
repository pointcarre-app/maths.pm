# Safari CSS Download Configuration

## Overview
The application downloads external CSS files locally to avoid CORS issues with Safari browser. This is particularly important for the deployed GitHub Pages site where Safari's strict CORS policies can prevent loading of external stylesheets.

## Behavior by Environment

### GitHub Actions / CI Environment
- **Detection**: `CI=true` or `GITHUB_ACTIONS=true` environment variables
- **Behavior**: ALWAYS downloads CSS files with `force_download=True`
- **Purpose**: Ensures the deployed site has all necessary CSS files locally
- **Error Handling**: Failures are treated as critical and will stop the deployment

### Local Development (Default)
- **Detection**: No CI environment variables detected
- **Behavior**: Checks if CSS files exist; only downloads if missing
- **Purpose**: Speeds up local development by avoiding unnecessary downloads
- **Error Handling**: Failures are logged as warnings but don't stop execution

### Local Development with Force Download
- **Configuration**: Set `DOWNLOAD_SAFARI_CSS=true` environment variable
- **Behavior**: Forces download of all CSS files
- **Purpose**: Useful for testing or refreshing CSS files locally
- **Usage Examples**:
  ```bash
  # Force download in local development
  DOWNLOAD_SAFARI_CSS=true python -m uvicorn src.app:app --reload
  
  # Or export for the session
  export DOWNLOAD_SAFARI_CSS=true
  python -m uvicorn src.app:app --reload
  ```

## Downloaded Files

The following CSS files are downloaded to `src/static/css/safari-local/`:

1. **Google Fonts**:
   - `fonts-comfortaa.css` - Multiple font families including Comfortaa, Cormorant Garamond, etc.
   - `fonts-lexend.css` - Lexend and Playfair Display fonts

2. **UI Framework**:
   - `daisyui.css` - DaisyUI CSS framework
   - `daisyui-themes.css` - DaisyUI theme definitions

3. **Math Rendering**:
   - `katex.min.css` - KaTeX for mathematical expressions

4. **Papyrus Styles**:
   - `papyrus-index.css` - Main Papyrus styles
   - `papyrus-print.css` - Print-specific Papyrus styles

Font files (woff2, etc.) referenced in CSS files are also downloaded to `src/static/css/safari-local/fonts/`.

## Implementation Details

The `download_safari_css_files()` function in `src/app.py`:
- Accepts a `force_download` parameter
- When `force_download=False`, checks if all files exist before downloading
- Downloads CSS files and their referenced font files
- Rewrites font URLs in CSS to use local copies

## Troubleshooting

### Files not downloading in GitHub Actions
- Check the workflow logs for error messages
- Ensure the GitHub Actions environment has network access
- The deployment will fail if downloads fail (by design)

### Files downloading every time locally
- Check if `DOWNLOAD_SAFARI_CSS` environment variable is set
- Remove the variable or set it to `false` to enable caching behavior

### Safari still showing CORS errors
- Verify files were downloaded to `src/static/css/safari-local/`
- Check that the Safari CSS loader script is properly included in templates
- Clear Safari cache and reload the page
