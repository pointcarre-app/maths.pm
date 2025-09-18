# PM From URL Implementation Guide

## Overview

The `/pm-from-url` route allows loading and rendering PM (Pedagogical Markdown) files from distant URLs, enabling dynamic content loading from external sources like GitHub repositories, content management systems, or any publicly accessible markdown files.

## Route Definition

**Endpoint:** `GET /pm-from-url`

**Location:** `src/core/router.py` (lines ~961-1128)

**Function:** `get_pm_from_url()`

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `url` | `str` | Yes | - | URL to fetch the markdown file from |
| `product_name` | `str` | No | `None` | Product name for loading product-specific settings |
| `format` | `str` | No | `"html"` | Response format (`json` or `html`) |
| `debug` | `bool` | No | `False` | Enable debug mode for verbose logging |

## Implementation Details

### 1. URL Validation

```python
parsed_url = urlparse(url)
if not parsed_url.scheme or not parsed_url.netloc:
    raise HTTPException(status_code=400, detail="Invalid URL format...")
```

- Uses `urllib.parse.urlparse()` to validate URL structure
- Ensures both scheme (http/https) and netloc (domain) are present
- Returns `400 Bad Request` for malformed URLs

### 2. Content Fetching

```python
async with httpx.AsyncClient(timeout=30.0) as client:
    response = await client.get(url)
    response.raise_for_status()
    markdown_content = response.text
```

- Uses `httpx.AsyncClient` for non-blocking HTTP requests
- 30-second timeout to prevent hanging requests
- Raises HTTP status exceptions for 4xx/5xx responses
- Extracts text content from response

### 3. Content Type Validation

```python
content_type = response.headers.get("content-type", "").lower()
if not (content_type.startswith("text/") or "markdown" in content_type):
    logger.warning(f"URL content-type is {content_type}, proceeding anyway")
```

- Checks `Content-Type` header for text-based content
- Warns but continues if content type is not text-based
- Allows flexibility for various server configurations

### 4. PM Building

```python
pm = PMBuilder.from_markdown(
    md_content=markdown_content,
    origin=url,
    verbosity=1 if debug else 0,
)
```

- Uses existing `PMBuilder.from_markdown()` method
- Sets the URL as the origin for tracking
- Enables verbose logging in debug mode

### 5. Product Integration

```python
product_settings = None
if product_name:
    product_settings = get_product_settings(product_name)
```

- Optionally loads product-specific settings
- Integrates with existing product configuration system
- Allows custom styling, behavior, and metadata per product

## Response Formats

### JSON Response

```json
{
  "title": "Document Title",
  "fragments": [...],
  "metadata": {...},
  "source_url": "https://example.com/file.md",
  "product_settings": {...}
}
```

**Features:**
- Complete PM object serialization
- Source URL tracking
- Optional product settings inclusion
- Same structure as local PM JSON responses

### HTML Response

**Template:** `pm/index.html`

**Context Variables:**
- `pm`: Complete PM object
- `pm_json`: JSON-serialized PM data
- `origin`: Source URL
- `source_url`: Source URL (duplicate for clarity)
- `product_name`: Product identifier
- `product_settings`: Product configuration
- `pm_metatags`: Extracted metadata for SEO
- `debug`: Debug mode flag

## Error Handling

### 400 Bad Request
- **Trigger:** Invalid URL format
- **Example:** `url=not-a-valid-url`
- **Response:** `{"detail": "Invalid URL format. URL must include scheme (http/https) and domain."}`

### 400 Bad Request (Network)
- **Trigger:** HTTP errors during fetching
- **Example:** 404 Not Found, connection timeout
- **Response:** `{"detail": "Failed to fetch content from URL: [error details]"}`

### 422 Unprocessable Entity
- **Trigger:** Markdown parsing failures
- **Example:** Invalid YAML metadata, malformed markdown
- **Response:** `{"detail": "Failed to parse markdown content: [error details]"}`

### 500 Internal Server Error
- **Trigger:** Unexpected system errors
- **Example:** Memory issues, filesystem problems
- **Response:** `{"detail": "Unexpected error fetching URL: [error details]"}`

## Usage Examples

### Basic HTML Rendering
```bash
GET /pm-from-url?url=https://raw.githubusercontent.com/user/repo/main/lesson.md
```

### JSON API Response
```bash
GET /pm-from-url?url=https://example.com/content.md&format=json
```

### With Product Settings
```bash
GET /pm-from-url?url=https://example.com/file.md&product_name=corsica&format=html
```

### Debug Mode
```bash
GET /pm-from-url?url=https://example.com/file.md&debug=true
```

## Security Considerations

### URL Validation
- Only allows `http://` and `https://` schemes
- Prevents local file access (`file://`) and other protocols
- Validates domain presence to prevent malformed requests

### Network Security
- 30-second timeout prevents DoS attacks
- No automatic redirects following (httpx default)
- Content-type validation (warning only, not blocking)

### Content Security
- No executable content processing
- Standard markdown parsing only
- Same security model as local PM files

## Performance Considerations

### Caching
- **Current:** No caching implemented
- **Recommendation:** Consider implementing HTTP cache headers or Redis caching for frequently accessed URLs
- **Implementation:** Could cache based on URL + ETag/Last-Modified headers

### Timeout Management
- 30-second timeout balances user experience with resource protection
- Async implementation prevents blocking other requests
- Consider implementing retry logic for transient failures

### Memory Usage
- Entire markdown content loaded into memory
- Consider streaming for very large files
- Monitor memory usage with large documents

## Integration Points

### Existing Systems
- **PM Builder:** Uses `PMBuilder.from_markdown()` - no changes needed
- **Product Settings:** Full compatibility with `get_product_settings()`
- **Templates:** Uses same `pm/index.html` template as local files
- **Metadata:** Full metatag extraction and SEO support

### Dependencies
- **httpx:** HTTP client library (already in project)
- **urllib.parse:** URL validation (Python standard library)
- **PMBuilder:** Existing PM building infrastructure
- **Product System:** Existing product configuration system

## Testing Strategy

### Manual Testing
```bash
# Test with GitHub raw files
curl "http://localhost:8000/pm-from-url?url=https://raw.githubusercontent.com/microsoft/vscode/main/README.md"

# Test JSON response
curl "http://localhost:8000/pm-from-url?url=https://example.com/file.md&format=json"

# Test error handling
curl "http://localhost:8000/pm-from-url?url=invalid-url"
```

### Automated Testing
- Unit tests for URL validation logic
- Integration tests with mock HTTP responses
- Error handling tests for various failure scenarios
- Performance tests with different file sizes

## Future Enhancements

### Caching Layer
```python
# Potential Redis caching implementation
cache_key = f"pm_url:{hashlib.md5(url.encode()).hexdigest()}"
cached_content = await redis.get(cache_key)
if cached_content:
    return cached_content
```

### Authentication Support
```python
# Potential header-based authentication
headers = {}
if auth_token:
    headers["Authorization"] = f"Bearer {auth_token}"
response = await client.get(url, headers=headers)
```

### Content Validation
```python
# Potential file size limits
if len(markdown_content) > MAX_FILE_SIZE:
    raise HTTPException(status_code=413, detail="File too large")
```

### Rate Limiting
```python
# Potential rate limiting per IP/user
@limiter.limit("10/minute")
async def get_pm_from_url(...):
```

## Troubleshooting

### Common Issues

**Issue:** "Invalid URL format" error
**Solution:** Ensure URL includes `http://` or `https://` scheme

**Issue:** "Failed to fetch content" error
**Solutions:**
- Check URL accessibility in browser
- Verify network connectivity
- Check for authentication requirements
- Verify content-type headers

**Issue:** "Failed to parse markdown" error
**Solutions:**
- Validate markdown syntax
- Check YAML metadata format
- Test with simpler markdown content
- Enable debug mode for detailed errors

### Debugging

**Enable Debug Mode:**
```bash
GET /pm-from-url?url=https://example.com/file.md&debug=true
```

**Check Logs:**
```bash
# Look for httpx and PMBuilder logs
tail -f server.log | grep -E "(httpx|PMBuilder|pm-from-url)"
```

**Validate URL Manually:**
```bash
curl -I "https://example.com/file.md"
```

## Monitoring

### Key Metrics
- Request count and success rate
- Average response time
- Error distribution by type
- Most frequently accessed URLs
- Cache hit/miss ratios (if implemented)

### Logging
- URL access attempts
- Network failures
- Parsing errors
- Performance metrics
- Security-related events

## Deployment Notes

### Production Considerations
- Monitor memory usage with large files
- Implement proper logging and monitoring
- Consider implementing rate limiting
- Set up alerts for high error rates
- Document URL whitelist if needed for security

### Configuration
- Timeout values may need adjustment based on network conditions
- Consider environment-specific product settings
- Monitor and adjust cache settings if implemented

## Related Documentation
- [PM_INCLUDE_TEMPLATES_GUIDE.md](./PM_INCLUDE_TEMPLATES_GUIDE.md) - Template system details
- [PRODUCT_METATAGS_IMPLEMENTATION.md](./PRODUCT_METATAGS_IMPLEMENTATION.md) - Metadata handling
- [SETTINGS_DOCUMENTATION.md](./SETTINGS_DOCUMENTATION.md) - Product configuration system
