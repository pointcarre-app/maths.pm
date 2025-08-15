# GitHub Pages Deployment - Quick Reference Guide

## 🚀 Deployment URL
**Live Site**: https://pointcarre-app.github.io/maths.pm/

## 📋 Pre-Deployment Checklist

### Local Testing
```bash
# 1. Clean build
rm -rf dist
python scripts/build_for_github.py

# 2. Verify critical files exist
ls -la dist/index.html
ls -la dist/pm/corsica/a_troiz_geo.html
ls -la dist/static/css/root.css
ls -la dist/.nojekyll

# 3. Check for localhost URLs (should return nothing)
grep -r "127.0.0.1" dist/
grep -r "localhost" dist/

# 4. Test locally
cd dist && python -m http.server 8080
# Visit: http://localhost:8080
```

## 🔄 Deployment Process

### Automatic (on push to main)
```bash
# Make changes
git add -A
git commit -m "Description of changes"
git push origin main

# GitHub Actions will automatically:
# 1. Run build_for_github.py
# 2. Deploy to GitHub Pages
# 3. Site updates in ~3-5 minutes
```

### Manual Trigger
1. Go to: https://github.com/pointcarre-app/maths.pm/actions
2. Select "Deploy static content to Pages"
3. Click "Run workflow"
4. Choose branch: main
5. Click "Run workflow"

## 🔍 Monitoring Deployment

### Check Build Status
```bash
# Via API
curl -s 'https://api.github.com/repos/pointcarre-app/maths.pm/actions/runs?per_page=1' | \
  python -c "import json,sys; r=json.load(sys.stdin)['workflow_runs'][0]; \
  print(f\"Status: {r['status']}, Conclusion: {r.get('conclusion', 'pending')}\")"
```

### Check Deployed Content
```bash
# Check if PM route is accessible
curl -I https://pointcarre-app.github.io/maths.pm/pm/corsica/a_troiz_geo.html

# Check build report
curl -s https://pointcarre-app.github.io/maths.pm/build-report.json | \
  python -m json.tool | head -20
```

## 🛠️ Common Issues & Solutions

### Issue: PM routes return 404
**Solution**: Ensure `.nojekyll` file exists in dist/
```bash
touch dist/.nojekyll
```

### Issue: CSS/JS files show ERR_BLOCKED_BY_ORB
**Solution**: Check for localhost URLs in HTML
```bash
# In build script, ensure these replacements:
content = content.replace("http://127.0.0.1:8000/", "/")
content = content.replace("http://localhost:8000/", "/")
```

### Issue: Build takes too long
**Solution**: Kill stuck processes
```bash
pkill -f "build_for_github"
pkill -f "jupyter-lite"
```

### Issue: Changes not reflected
**Solution**: Clear browser cache or wait 5 minutes for CDN

## 📁 Key Files & Directories

```
Project Structure:
├── scripts/
│   └── build_for_github.py      # Main build script (hardcoded routes)
├── .github/workflows/
│   └── static.yml                # GitHub Actions workflow
├── pms/                          # Source PM content
│   ├── corsica/                  # Corsica exercises
│   ├── documentation/            # Documentation
│   └── pyly/                     # Python curriculum
├── src/static/                   # Static assets (CSS, JS, images)
├── dist/                         # Build output (git-ignored)
└── notes/                        # Documentation
    ├── PM_ROUTES_DEPLOYMENT_FIX.md
    └── GITHUB_PAGES_DEPLOYMENT_GUIDE.md
```

## 🎯 Quick Commands

```bash
# Full rebuild and test
rm -rf dist && python scripts/build_for_github.py && \
  echo "Files: $(find dist -name "*.html" | wc -l) HTML" && \
  echo "Check: $(grep -r '127.0.0.1' dist/ | wc -l) localhost URLs (should be 0)"

# Check what PM files exist
find pms -name "*.md" | head -10

# Test specific PM route locally
curl -s http://localhost:8000/pm/corsica/a_troiz_geo.md | head -20
```

## 📊 Expected Build Output

```
Total routes: 60+
HTML files created: 62
PM files: 39 (25 markdown + 14 assets)
Static files: All CSS, JS, SVG copied
Build time: ~30-60 seconds locally
```

## 🔗 Important URLs

- **Live Site**: https://pointcarre-app.github.io/maths.pm/
- **PM Example**: https://pointcarre-app.github.io/maths.pm/pm/corsica/a_troiz_geo.html
- **GitHub Repo**: https://github.com/pointcarre-app/maths.pm
- **Actions**: https://github.com/pointcarre-app/maths.pm/actions
- **Pages Settings**: https://github.com/pointcarre-app/maths.pm/settings/pages

## ⚠️ Critical Rules

1. **ALWAYS** include `.nojekyll` in dist/
2. **ALWAYS** strip localhost URLs from HTML
3. **ALWAYS** use `/maths.pm/` as base path for GitHub Pages
4. **NEVER** use dynamic route generation - hardcode them
5. **NEVER** trust that fetching will work - copy files as backup

## ✅ Success Indicators

When deployment is successful:
- No 404 errors in browser console
- No ERR_BLOCKED_BY_ORB errors
- All CSS styles load (page looks styled)
- Interactive elements work (buttons, forms)
- PM content displays with proper formatting
- Images and SVGs load correctly

---
*Last updated: August 15, 2024*  
*Verified working deployment*

