# PM From URL - Security & Environment Management

## Overview

The PM-from-URL functionality now includes robust security features that protect GitHub tokens in production environments while providing convenient development tools.

## Environment-Based Security

### Environment Detection

The system uses the `ENVIRONMENT` variable to determine security behavior:

```bash
# .env file
ENVIRONMENT=development  # or staging, test, production
GITHUB_TOKEN=ghp_your_token_here
```

### Security Rules

| Environment | GitHub Token from ENV | Behavior |
|------------|----------------------|----------|
| `development` | ✅ Allowed | Auto-loads token for convenience |
| `staging` | ✅ Allowed | Auto-loads token for testing |
| `test` | ✅ Allowed | Auto-loads token for testing |
| `production` | ❌ Blocked | Must use `github_token` parameter |

### Production Security

In production, the system:
- **Blocks** automatic token loading from environment
- **Requires** explicit `github_token` parameter for private repos
- **Raises 403 error** if environment token is present without parameter

```python
# Production behavior
if environment == "production" and os.getenv("GITHUB_TOKEN") and not github_token:
    raise HTTPException(
        status_code=403,
        detail="GitHub token from environment is not allowed in production. Use github_token parameter instead."
    )
```

## Test Interface

### Access Control

The test interface at `/pm-from-url-test` is **environment-protected**:

- ✅ **Available**: development, staging, test
- ❌ **Blocked**: production (returns 403)

### Features

1. **Public Repository Testing**
   - No token required
   - Pre-filled with VSCode README example
   - Product name selection

2. **Private Repository Testing**
   - Uses environment token automatically
   - Pre-filled with your private repo URL
   - Disabled if no token available

3. **Manual URL Builder**
   - Custom URL construction
   - Product and format selection
   - Copy/open functionality

4. **Environment Information**
   - Current environment display
   - Token availability status
   - Security warnings

## Usage Examples

### Development Environment

```bash
# .env file
ENVIRONMENT=development
GITHUB_TOKEN=ghp_your_token_here

# Automatic token usage (no parameter needed)
curl "http://127.0.0.1:5001/pm-from-url?url=https://raw.githubusercontent.com/user/private-repo/main/file.md"

# Test interface available
open http://127.0.0.1:5001/pm-from-url-test
```

### Production Environment

```bash
# .env file (or environment variables)
ENVIRONMENT=production
# GITHUB_TOKEN should NOT be set

# Must use parameter for private repos
curl "http://127.0.0.1:5001/pm-from-url?url=https://raw.githubusercontent.com/user/private-repo/main/file.md&github_token=ghp_token"

# Test interface blocked (returns 403)
curl http://127.0.0.1:5001/pm-from-url-test  # 403 Forbidden
```

## Security Benefits

### Token Protection
- **No accidental exposure** in production logs
- **Explicit consent** required for token usage in production
- **Environment isolation** prevents token leakage

### Access Control
- **Development tools** only available in safe environments
- **Production hardening** prevents test interfaces in live systems
- **Clear error messages** guide proper usage

### Audit Trail
- **Debug logging** shows token source (parameter vs environment)
- **Environment tracking** in logs and responses
- **Security events** logged for monitoring

## Configuration

### Environment Variables

```bash
# Required
ENVIRONMENT=development  # development, staging, test, production

# Optional (only loaded in non-production)
GITHUB_TOKEN=ghp_your_github_token_here
```

### Deployment Considerations

1. **Development/Staging**
   - Set `ENVIRONMENT=development` or `ENVIRONMENT=staging`
   - Include `GITHUB_TOKEN` in environment
   - Test interface will be available

2. **Production**
   - Set `ENVIRONMENT=production`
   - **DO NOT** set `GITHUB_TOKEN` in environment
   - Use `github_token` parameter when needed
   - Test interface will be blocked

## Error Messages

### Production Token Block
```json
{
  "detail": "GitHub token from environment is not allowed in production. Use github_token parameter instead."
}
```

### Test Interface Block
```json
{
  "detail": "PM-from-URL test interface is only available in development, staging, and test environments."
}
```

## Migration Guide

### From Previous Version

1. **Add environment variable**:
   ```bash
   echo "ENVIRONMENT=development" >> .env
   ```

2. **Update URLs** (if using local testing):
   - Change `localhost` → `127.0.0.1`
   - Change port `8080` → `8021`

3. **Use test interface**:
   ```bash
   open http://127.0.0.1:5001/pm-from-url-test
   ```

### Production Deployment

1. **Set production environment**:
   ```bash
   export ENVIRONMENT=production
   ```

2. **Remove GitHub token** from environment variables

3. **Use parameter-based authentication**:
   ```bash
   curl "http://your-domain.com/pm-from-url?url=https://raw.githubusercontent.com/user/repo/main/file.md&github_token=ghp_token"
   ```

This security system ensures that GitHub tokens are handled safely across different deployment environments while maintaining development convenience.
