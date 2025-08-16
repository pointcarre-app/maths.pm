# Nagini with esm.sh CDN

## ✅ Current Configuration

Using **esm.sh CDN** which automatically handles ES module imports:
- **Version**: v0.0.20
- **CDN URL**: `https://esm.sh/gh/pointcarre-app/nagini@v0.0.20/src/nagini.js`
- **Worker URL**: `https://cdn.jsdelivr.net/gh/pointcarre-app/nagini@v0.0.20/src/pyodide/worker/worker-dist.js`

## Why esm.sh?

esm.sh is a CDN that:
1. **Automatically resolves ES module imports** - No more "Cannot use import statement" errors
2. **Bundles dependencies on-the-fly** - All local imports are resolved
3. **Provides proper module exports** - Works with modern ES module syntax
4. **Handles TypeScript/JSX** - Can transform various module formats

## What's Working

1. ✅ **Nagini Core Loading** - Via esm.sh CDN
2. ✅ **Basic Python Execution** - Simple code runs successfully  
3. ✅ **Pyodide Integration** - Python interpreter works in browser
4. ✅ **Worker Communication** - Messages pass correctly

## Known Issues

1. **Package Loading** - Sympy/Pydantic may need manual installation after manager creation
2. **Console Warnings** - Some warnings from internal Nagini code are expected

## Test Results

- **Basic Python Test**: ✅ Successfully executes `42 * 2 = 84`
- **Worker Setup**: ✅ Creates and initializes properly
- **Module Import**: ✅ esm.sh handles all internal imports

## Configuration in `products/01_sujets0.yml`

```yaml
backend_settings:
  nagini:
    endpoint: "https://cdn.jsdelivr.net/gh/pointcarre-app/nagini@v0.0.20/"
    js_url: "https://esm.sh/gh/pointcarre-app/nagini@v0.0.20/src/nagini.js"
    pyodide_worker_url: "https://cdn.jsdelivr.net/gh/pointcarre-app/nagini@v0.0.20/src/pyodide/worker/worker-dist.js"
```

## If Issues Persist

1. **Check Network Tab** - Ensure esm.sh is responding
2. **Verify URL Format** - Must be `https://esm.sh/gh/[user]/[repo]@[version]/[path]`
3. **Try Direct NPM** - If published: `https://esm.sh/nagini@0.0.20`
4. **Check Console** - Look for specific import errors

## Alternative CDNs

If esm.sh doesn't work:
- **Skypack**: `https://cdn.skypack.dev/...`
- **jsDelivr with ESM**: `https://cdn.jsdelivr.net/npm/...`
- **unpkg**: `https://unpkg.com/...`