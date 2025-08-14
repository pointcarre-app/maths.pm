# Deployment Guide for Maths.pm

This guide explains how the static site generation and GitHub Pages deployment works for the Maths.pm application.

## 🚀 Automatic Deployment

The site is automatically deployed to GitHub Pages when you push to the `main` branch. The deployment process is handled by GitHub Actions.

### GitHub Actions Workflow

The workflow file is located at `.github/workflows/deploy.yml` and performs the following steps:

1. **Checkout Code**: Fetches the latest code from the repository
2. **Setup Python**: Installs Python 3.13 with pip caching
3. **Install Dependencies**: Installs all required Python packages
4. **Build Static Site**: 
   - Starts the FastAPI server in the background
   - Calls the `/api/build` endpoint to generate static files
   - Saves all HTML, JSON, and static assets to the `dist` directory
5. **Verify Build**: Checks that the `dist` directory was created and contains files
6. **Deploy to GitHub Pages**: Publishes the `dist` directory to GitHub Pages

## 🧪 Local Testing

Before pushing changes, you can test the static site generation locally:

### Method 1: Using the Test Script (Recommended)

```bash
# Run from project root
./scripts/test_build.sh
```

This script will:
- Create a virtual environment
- Install dependencies
- Run the build process
- Show build statistics
- Provide instructions for testing the static site

### Method 2: Manual Build

```bash
# Install dependencies
pip install -r requirements.txt

# Run the build script
python scripts/build_static.py

# Serve the static files locally
python -m http.server 8080 -d dist
```

Then visit http://localhost:8080 to view the static site.

## 📁 Build Output Structure

The static build creates a `dist` directory with the following structure:

```
dist/
├── index.html              # Main page
├── readme.html             # README page
├── settings.html           # Settings page
├── sujets0.html           # Sujets0 page
├── corsica.html           # Corsica module
├── nagini.html            # Nagini module
├── pm/                    # PM documentation
│   ├── index.html         # PM root
│   ├── documentation/     # Documentation files
│   ├── examples/          # Example files
│   ├── pyly/             # Python curriculum
│   └── corsica/          # Corsica exercises
├── jupyterlite/          # JupyterLite integration
├── api/                  # API endpoints (JSON)
│   ├── health.json
│   ├── products.json
│   └── settings.json
├── static/               # Static assets
│   ├── css/             # Stylesheets
│   ├── js/              # JavaScript files
│   ├── icons/           # Icons and images
│   └── jupyterlite/     # JupyterLite assets
└── build-report.json    # Build statistics

```

## 🔧 Configuration

### Routes to Export

The routes to be included in the static build are defined in `src/build.py`:

```python
routes = [
    "/",                    # Main page
    "/readme",             # Documentation
    "/settings",           # Settings page
    "/sujets0",           # Sujets0 module
    "/corsica",           # Corsica module
    "/nagini",            # Nagini module
    "/api/health",        # API endpoints
    "/api/products",
    "/api/settings",
    "/kill-service-workers",
    "/pm",                # PM root
    # JupyterLite routes
    "/jupyterlite/",
    "/jupyterlite/lab",
    "/jupyterlite/repl",
    # PM documentation routes
    "/pm/documentation/README",
    "/pm/examples/i_radio_example",
    # ... etc
]
```

To add new routes, edit the `routes` list in `src/build.py`.

### GitHub Pages Settings

1. Go to your repository settings on GitHub
2. Navigate to "Pages" in the sidebar
3. Source should be set to "GitHub Actions"
4. The site will be available at: `https://[username].github.io/[repository-name]/`

## 🐛 Troubleshooting

### Build Fails Locally

1. **Check Python version**: Ensure you're using Python 3.10+
   ```bash
   python --version
   ```

2. **Check dependencies**: Reinstall requirements
   ```bash
   pip install --force-reinstall -r requirements.txt
   ```

3. **Check server is not already running**: Kill any existing processes on port 8000
   ```bash
   lsof -ti:8000 | xargs kill -9
   ```

### Build Fails in GitHub Actions

1. Check the Actions tab in GitHub for detailed error logs
2. Common issues:
   - **Import errors**: Ensure all imports use `from src import ...` not `from app import ...`
   - **Missing dependencies**: Check that all required packages are in `requirements.txt`
   - **Route errors**: Verify that all routes in the build list actually exist

### Static Site Issues

1. **Missing styles/JavaScript**: Check that static files are being copied correctly
2. **Broken links**: Ensure all internal links use relative paths
3. **404 errors**: Verify that the route is included in the build configuration

## 📊 Build Report

After each build, a `build-report.json` file is created in the `dist` directory containing:

```json
{
  "status": "success",
  "total_routes": 25,
  "successful": 25,
  "failed": 0,
  "output_dir": "dist",
  "routes": [
    {"route": "/", "success": true},
    {"route": "/readme", "success": true},
    // ... etc
  ]
}
```

## 🔒 Security Notes

- The `.nojekyll` file prevents GitHub Pages from processing files with Jekyll
- The `dist` directory is in `.gitignore` and should not be committed
- Sensitive settings should use environment variables, not hardcoded values

## 📝 Manual Deployment (Emergency)

If the GitHub Actions workflow fails, you can manually deploy:

```bash
# Build locally
python scripts/build_static.py

# Create gh-pages branch if it doesn't exist
git checkout --orphan gh-pages

# Remove all files
git rm -rf .

# Add built files
cp -r dist/* .
echo "maths.pm" > CNAME  # If using custom domain

# Commit and push
git add .
git commit -m "Manual deployment"
git push origin gh-pages --force

# Return to main branch
git checkout main
```

## 🚦 Status Monitoring

You can monitor the deployment status:

1. **GitHub Actions**: Check the Actions tab for workflow runs
2. **GitHub Pages**: Settings → Pages shows deployment status
3. **API Health**: Visit `/api/health` on the deployed site

## 📧 Support

For deployment issues, check:
1. This documentation
2. GitHub Actions logs
3. The build report in `dist/build-report.json`
4. Server logs if running locally
