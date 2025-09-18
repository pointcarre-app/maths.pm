# PM From URL - GitHub Private Repository Guide

## The Problem

Your URL: `https://github.com/pointcarre-app/mathspm-pp/tree/main/test-pms`

**Issues:**
1. **Tree URL**: This shows a directory listing, not a raw file
2. **Private Repository**: Requires authentication to access
3. **No File Extension**: Points to a folder, not a specific markdown file

## Solutions

### Option 1: Use GitHub Raw URLs (Recommended)

For private repositories, you need **raw file URLs** with authentication:

```bash
# Format for private repo raw files
https://raw.githubusercontent.com/pointcarre-app/mathspm-pp/main/test-pms/your-file.md
```

**But this requires authentication!**

### Option 2: GitHub Personal Access Token

Create a GitHub Personal Access Token and modify the PM-from-URL route to support authentication.

#### Step 1: Create GitHub Token
1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Generate new token (classic)
3. Select scopes: `repo` (for private repositories)
4. Copy the token

#### Step 2: Test with curl (manual)
```bash
# Test direct access with token
curl -H "Authorization: token YOUR_GITHUB_TOKEN" \
  "https://raw.githubusercontent.com/pointcarre-app/mathspm-pp/main/test-pms/sample-file.md"
```

### Option 3: Modify PM-from-URL Route for Authentication

Add GitHub token support to your route:

```python
@core_router.get("/pm-from-url")
async def get_pm_from_url(
    request: Request,
    url: str = Query(..., description="URL to fetch the markdown file from"),
    github_token: str = Query(None, description="GitHub personal access token for private repos"),
    product_name: str = Query(None, description="Product name for settings"),
    format: str = Query("html", description="Response format (json or html)", regex="^(json|html)$"),
    debug: bool = Query(False, description="Debug mode"),
) -> Response:
    # ... existing validation code ...
    
    # Prepare headers for authentication
    headers = {}
    if github_token and "github.com" in url:
        headers["Authorization"] = f"token {github_token}"
    
    # Fetch content with authentication
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            markdown_content = response.text
    except httpx.HTTPError as e:
        if response.status_code == 404:
            raise HTTPException(
                status_code=404, 
                detail="File not found. Check URL and authentication for private repos."
            )
        # ... rest of error handling
```

### Option 4: Environment Variable for Token

More secure approach - use environment variable:

```python
import os

# In your route
github_token = os.getenv("GITHUB_TOKEN")
if github_token and "github.com" in url:
    headers["Authorization"] = f"token {github_token}"
```

Then set the environment variable:
```bash
export GITHUB_TOKEN="your_github_token_here"
python -m src.app
```

## Correct URLs for Your Repository

Assuming you have files in `mathspm-pp/test-pms/`, the correct URLs would be:

```bash
# For a file named "lesson1.md"
https://raw.githubusercontent.com/pointcarre-app/mathspm-pp/main/test-pms/lesson1.md

# For a file named "sample.md"
https://raw.githubusercontent.com/pointcarre-app/mathspm-pp/main/test-pms/sample.md
```

## Testing Private Repository Access

### Step 1: Create a test file in your private repo
```markdown
# test-pms/sample-private.md
---
title: "Private Repository Test"
description: "Testing PM from private GitHub repo"
---

# Private Content Test

This content is loaded from a private GitHub repository!
```

### Step 2: Test with authentication
```bash
# With token parameter (if you modify the route)
curl "http://localhost:5001/pm-from-url?url=https://raw.githubusercontent.com/pointcarre-app/mathspm-pp/main/test-pms/sample-private.md&github_token=YOUR_TOKEN"

# With environment variable (if you use that approach)
export GITHUB_TOKEN="your_token_here"
curl "http://localhost:5001/pm-from-url?url=https://raw.githubusercontent.com/pointcarre-app/mathspm-pp/main/test-pms/sample-private.md"
```

## Security Considerations

### Token Security
- **Never commit tokens to git**
- Use environment variables in production
- Consider using GitHub Apps for better security
- Rotate tokens regularly

### URL Validation
- Validate GitHub URLs specifically
- Check for proper raw.githubusercontent.com format
- Prevent token leakage in logs

### Rate Limiting
- GitHub has API rate limits
- Consider caching responses
- Implement proper error handling for rate limit errors

## Alternative: Make Repository Public

**Simplest solution:** Make your `mathspm-pp` repository public, then:

```bash
# No authentication needed
curl "http://localhost:5001/pm-from-url?url=https://raw.githubusercontent.com/pointcarre-app/mathspm-pp/main/test-pms/your-file.md"
```

## Current Status

**Without modifications**, your PM-from-URL route will:
- ❌ Fail with private GitHub URLs (401 Unauthorized)
- ✅ Work with public GitHub raw URLs
- ✅ Work with any public raw markdown URLs

## Recommended Implementation

Add GitHub token support to your existing route:

```python
# Add this parameter to your existing route
github_token: str = Query(None, description="GitHub token for private repos")

# Add this in the fetch section
headers = {}
if github_token and "githubusercontent.com" in url:
    headers["Authorization"] = f"token {github_token}"

async with httpx.AsyncClient(timeout=30.0) as client:
    response = await client.get(url, headers=headers)  # Pass headers
```

## Testing Commands

```bash
# Public repository (works now)
curl "http://localhost:5001/pm-from-url?url=https://raw.githubusercontent.com/microsoft/vscode/main/README.md"

# Private repository (needs token)
curl "http://localhost:5001/pm-from-url?url=https://raw.githubusercontent.com/pointcarre-app/mathspm-pp/main/test-pms/file.md&github_token=YOUR_TOKEN"

# With product settings
curl "http://localhost:5001/pm-from-url?url=https://raw.githubusercontent.com/pointcarre-app/mathspm-pp/main/test-pms/file.md&github_token=YOUR_TOKEN&product_name=dataviz2"
```

Would you like me to implement the GitHub token authentication in your PM-from-URL route?
