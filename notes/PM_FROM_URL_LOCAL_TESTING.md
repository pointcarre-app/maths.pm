# PM From URL - Local Testing Guide

## Quick Setup

This guide shows how to test the PM-from-URL functionality locally using a `products-private` folder and Python's built-in HTTP server.

## Directory Structure

```
/Users/selim/madles/
├── pca-mathspm/           # Your main repo
└── products-private/      # Private content folder (git-ignored)
    └── test-pms/
        ├── sample-lesson.md
        ├── simple-example.md
        └── ... (your test files)
```

## Step 1: Create Test Content

I've already created sample files in `/Users/selim/madles/products-private/test-pms/`:

### `sample-lesson.md`
- Complete PM with YAML metadata
- Math formulas, code blocks
- Interactive elements
- Good for testing full functionality

### `simple-example.md`
- Minimal markdown file
- Basic formatting
- Good for quick tests

## Step 2: Start Local HTTP Server

```bash
# Navigate to the products-private directory
cd /Users/selim/madles/products-private

# Start Python HTTP server on port 8080
python3 -m http.server 8080

# Or use a different port if 8080 is busy
python3 -m http.server 9000
```

**Server Output:**
```
Serving HTTP at 0.0.0.0 port 8080 (http://0.0.0.0:8080/) ...
```

## Step 3: Start Your Main Application

In another terminal:

```bash
# Navigate to your main repo
cd /Users/selim/madles/pca-mathspm

# Start your FastAPI application
python -m src.app
# OR however you normally start it
```

## Step 4: Test the PM-from-URL Route

### Basic HTML Test

```bash
# Test with the sample lesson
curl "http://localhost:5001/pm-from-url?url=http://localhost:8080/test-pms/sample-lesson.md"

# Test with the simple example
curl "http://localhost:5001/pm-from-url?url=http://localhost:8080/test-pms/simple-example.md"
```

### JSON API Test

```bash
# Get JSON response
curl "http://localhost:5001/pm-from-url?url=http://localhost:8080/test-pms/sample-lesson.md&format=json" | jq .

# Test with product settings
curl "http://localhost:5001/pm-from-url?url=http://localhost:8080/test-pms/sample-lesson.md&format=json&product_name=dataviz2" | jq .
```

### Browser Testing

Open in your browser:

```
# HTML view
http://localhost:5001/pm-from-url?url=http://localhost:8080/test-pms/sample-lesson.md

# With product settings (dataviz2 from your current file)
http://localhost:5001/pm-from-url?url=http://localhost:8080/test-pms/sample-lesson.md&product_name=dataviz2

# Debug mode
http://localhost:5001/pm-from-url?url=http://localhost:8080/test-pms/sample-lesson.md&debug=true
```

## Step 5: Test Error Handling

### Invalid URL Test
```bash
curl "http://localhost:5001/pm-from-url?url=not-a-valid-url"
# Expected: 400 Bad Request
```

### Non-existent File Test
```bash
curl "http://localhost:5001/pm-from-url?url=http://localhost:8080/test-pms/nonexistent.md"
# Expected: 400 Bad Request (404 from HTTP server)
```

### Server Down Test
```bash
# Stop the HTTP server (Ctrl+C) then try:
curl "http://localhost:5001/pm-from-url?url=http://localhost:8080/test-pms/sample-lesson.md"
# Expected: 400 Bad Request (Connection refused)
```

## Advanced Testing

### Custom Port Testing
```bash
# Start HTTP server on different port
cd /Users/selim/madles/products-private
python3 -m http.server 9000

# Test with new port
curl "http://localhost:5001/pm-from-url?url=http://localhost:9000/test-pms/sample-lesson.md"
```

### CORS Testing (if needed)
```bash
# Python HTTP server doesn't set CORS headers by default
# If you need CORS, use this alternative:
python3 -c "
import http.server
import socketserver
from http.server import SimpleHTTPRequestHandler

class CORSRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

with socketserver.TCPServer(('', 8080), CORSRequestHandler) as httpd:
    print('Serving with CORS at http://localhost:8080')
    httpd.serve_forever()
"
```

## Creating Your Own Test Files

### Basic Template
```markdown
---
title: "Your Title"
description: "Your description"
class_at_school: "seconde"
theme: "your_theme"
---

# Your Content

Your markdown content here...
```

### With Product-Specific Metadata
```markdown
---
title: "DataViz2 Test"
description: "Testing with dataviz2 product"
product: "dataviz2"
visualization_type: "interactive"
---

# DataViz2 Content

This will work well with `?product_name=dataviz2`
```

## Monitoring and Debugging

### HTTP Server Logs
The Python HTTP server shows access logs:
```
127.0.0.1 - - [18/Sep/2025 10:30:15] "GET /test-pms/sample-lesson.md HTTP/1.1" 200 -
```

### FastAPI Logs
Check your FastAPI application logs for PM processing:
```bash
# If you're logging to a file
tail -f server.log | grep pm-from-url

# Or check console output
```

### Debug Mode
Use `debug=true` parameter to see verbose PM building logs:
```bash
curl "http://localhost:8000/pm-from-url?url=http://localhost:8080/test-pms/sample-lesson.md&debug=true"
```

## Integration with Your Workflow

### Testing Different Products
Based on your current `products/04_dataviz2.yml`, you can test:

```bash
# Test with dataviz2 product settings
curl "http://localhost:5001/pm-from-url?url=http://localhost:8080/test-pms/sample-lesson.md&product_name=dataviz2"

# Test with other products
curl "http://localhost:5001/pm-from-url?url=http://localhost:8080/test-pms/sample-lesson.md&product_name=corsica"
```

### Comparing with Local Files
Compare the URL-loaded PM with local files:

```bash
# Local PM
curl "http://localhost:5001/pm/dataviz2/00_plan.md?format=json" | jq .title

# URL PM
curl "http://localhost:5001/pm-from-url?url=http://localhost:8080/test-pms/sample-lesson.md&format=json" | jq .title
```

## Security Notes

### Local Testing Only
- The Python HTTP server is for testing only
- Don't use in production
- No authentication or security features

### Network Access
- HTTP server is accessible from your local network
- Use `python3 -m http.server 8080 --bind 127.0.0.1` to restrict to localhost only

## Troubleshooting

### Common Issues

**Issue:** "Connection refused"
**Solution:** Make sure the HTTP server is running on the correct port

**Issue:** "File not found" 
**Solution:** Check file paths and HTTP server directory

**Issue:** "Invalid URL format"
**Solution:** Ensure URL includes `http://` prefix

**Issue:** PM parsing errors
**Solution:** Check YAML metadata syntax in your markdown files

### Quick Diagnostics

```bash
# Test HTTP server directly
curl http://localhost:8080/test-pms/sample-lesson.md

# Test main app health
curl http://localhost:5001/

# Check if file is accessible
ls -la /Users/selim/madles/products-private/test-pms/
```

## Next Steps

1. **Create More Test Files:** Add different types of content to test edge cases
2. **Test with Real URLs:** Try with actual GitHub raw files or other public URLs  
3. **Performance Testing:** Test with larger files to check timeout behavior
4. **Integration Testing:** Test with your actual product configurations

## Example Commands Summary

```bash
# Terminal 1: Start HTTP server
cd /Users/selim/madles/products-private
python3 -m http.server 8080

# Terminal 2: Start your app
cd /Users/selim/madles/pca-mathspm
python -m src.app

# Terminal 3: Test
curl "http://localhost:5001/pm-from-url?url=http://localhost:8080/test-pms/sample-lesson.md"
```

That's it! You now have a complete local testing environment for the PM-from-URL functionality.
