# Open Source Preparation Checklist

This document outlines all the issues that need to be addressed before releasing this project as open source. While this will be an unstable version, these items should be reviewed and addressed to ensure a proper release.

## Security and Sensitive Information

### Hard-coded Secrets and Credentials
- [x] **Development Secret Key** in `/src/corsica/get_block_migration/backend/config/config.py`:
  - Line 51: `SECRET_KEY: str = os.getenv("SECRET_KEY", "something")`
  - This default secret key should be removed or randomized for each installation
- [x] **S3 Endpoint URL** in `/src/corsica/get_block_migration/backend/config/config.py`:
  - Line 70: `S3_ENDPOINT: str = "stg"`
  - This appears to be a private S3 endpoint that should be externalized

### Internal References and URLs
- [ ] **Company Email and Contact Information** in `/domains/maths.pm.yml`:
  - Lines 14, 17, 57, 121: References to `contact(at)pointcarre.app`
  - Lines 11, 16-18: References to "SAS POINTCARRE.APP"
  - Lines 63-67: Office location details for Paris
- [ ] **Company Domain References**:
  - Multiple files reference `maths.pm` domain which should be generalized
  - `/src/settings.py` has hardcoded references to the domain

### Configuration That Should Be Externalized
- [ ] **Configuration Parameters** that should be moved to environment variables:
  - JupyterLite settings in `settings.py` (versions, packages)
  - Domain name settings (currently hardcoded as "maths.pm")
  - Static file paths and directories

## Licensing and Copyright Issues

### License Headers
- [ ] **Missing License Headers** in many files:
  - Only 6 files have the proper SPDX license identifier
  - Many JavaScript, CSS, and Python files lack proper license headers
  - AGPL-3.0 requires all source files to include license information
- [ ] **Copyright Notice** in LICENSE file:
  - Line 7: "Copyright (C) 2025 SAS POINTCARRE.APP"
  - Needs to be updated across all files

## Developer and Personal References


## Security Vulnerabilities

- [ ] **CORS Configuration**:
  - `ALLOWED_HOSTS: list[str] = ["*"]` in migration config allows all hosts
  - No proper CORS setup in the FastAPI application
- [ ] **Dependency Issues**:
  - External CDN links without integrity hashes in templates
  - Using older versions of libraries (Tailwind, DaisyUI) without pinned versions

## Structure and Documentation Issues

- [ ] **Incomplete Documentation**:
  - The README mentions security practices but doesn't fully implement them
  - Missing contribution guidelines for AGPL compliance

## Code Quality Issues

- [ ] **Debug Statements**:
  - Debug logging is enabled by default in `app.py` (line 29) - should be changed to INFO for production
  - Multiple `console.log` statements in JavaScript files like `mason.js` and `question-factory.js`
- [ ] **Incomplete Development Setup**:
  - Incomplete development requirements in `requirements-dev.txt` with a TODO comment
  - Missing linting configuration (no `.eslintrc`, `.flake8`, etc.)

## Hardcoded Values and External Dependencies

- [x] **Hardcoded Values**:
  - OK for now: Hardcoded prefix in `question-factory.js` (line 38): "The '1ere_' prefix is currently hardcoded"
  - OK for now: Hardcoded external CDN URL in `import-helper.js` (line 13): `https://cdn.jsdelivr.net/gh/pointcarre-app/nagini@0.0.18/src/nagini.js`
  - OK for now: Hardcoded URL in `drawer-tests-loader.js` (line 54): "Using hardcoded URL in JS"
  - OK for now: Hardcoded fallback API data URL in `mason.js` (line 82): `/static/curriculums/puissance_troiz.json`

## Documentation and Testing

- [ ] **Documentation Issues**:
  - No clear developer documentation on setup and contribution workflow
  - Incomplete documentation in `requirements-dev.txt` with version check TODO
  - Missing API documentation for backend endpoints
  - Missing comprehensive getting started guide for new developers
- [ ] **Testing Issues**:
  - No automated tests for Python or JavaScript code
  - No test framework configuration (pytest, jest, etc.)
  - No CI/CD configuration for running tests

## Additional Security Considerations

- [ ] **User Data Handling**:
  - Extensive browser metadata collection in `question-factory.js` including user agent, screen info, etc.
  - No CSRF protection visible in API endpoints
  - Security review needed for user-provided content handling

## Performance and Scalability

- [ ] **Performance Issues**:
  - Large file listing in `build_jupyterlite()` without pagination (lines 109-112)
  - No caching strategy for static assets
  - No rate limiting for API endpoints

## Configuration Management

- [ ] **Environment Configuration**:
  - Incomplete environment variable support (mostly hardcoded configuration)
  - No proper separation of dev/prod/test environments
  - Debugging settings enabled by default

## Code Maintenance

- [ ] **Duplicated Code**:
  - Duplicated files between `pms/` and `src/static/pm/` requiring manual syncing
  - Several commented-out code sections like in `mason.js` (line 106)
  - Some legacy/deprecated methods like `createFromPyodideLegacy` in `question-factory.js`

## Dependency Management

- [ ] **Dependency Issues**:
  - External CDN dependency on `nagini` without fallback
  - No pinned dependency versions in some cases
  - Missing proper package metadata (setup.py, package.json)
- [ ] **Licensing Compatibility**:
  - Need to verify all third-party dependencies are compatible with AGPL-3.0

## Recommendations by Priority

### Critical (Fix Before Release)
1. Remove all hardcoded credentials and secrets
2. Properly externalize configuration to environment variables
3. Add SPDX license headers to all source files
4. Fix personal information in domains/maths.pm.yml
5. Update copyright notices across the codebase

### Important
1. Implement proper CORS security
2. Remove personal directory paths
3. Add integrity hashes to CDN resources
4. Address developer TODOs and cleanup comments
5. Review and address security vulnerabilities

### Desirable
1. Improve documentation for AGPL compliance
2. Standardize directory structure
3. Clean up duplicate files
4. Complete the security checklist mentioned in README
5. Add proper tests and CI/CD configuration