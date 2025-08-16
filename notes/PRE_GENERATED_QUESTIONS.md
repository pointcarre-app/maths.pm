# Pre-Generated Questions System Documentation

## Overview

The pre-generated questions system allows for instant loading of mathematics questions without requiring Python execution in the browser. Questions are generated at build time using the `src/build_questions.py` script.

## Architecture

```
Build Time                          Runtime
----------                          --------
generators/*.py                     Browser
     ↓                                ↓
build_questions.py  →  JSON files  →  Fetch & Display
     ↓                                ↓
static/sujets0/questions/           Instant Loading
```

## File Structure

```
src/static/sujets0/questions/
├── index.json                          # Master index of all generators
├── spe_sujet1_auto_01_question/       # Generator directory
│   ├── metadata.json                  # Generator info & statistics
│   ├── 0.json                         # Question with seed 0
│   ├── 1.json                         # Question with seed 1
│   └── ... (up to 99.json)           # 100 questions per generator
└── [50+ more generator directories]
```

## Build Process

### Running the Build

```bash
# Generate all questions (takes ~2-3 minutes)
python src/build_questions.py

# Output:
# ✨ Build complete!
# 📊 Total questions generated: 4874
# 📁 Output location: /path/to/src/static/sujets0/questions
```

### Build Statistics

- **Generators processed**: 59 total
- **Successful generators**: 50 (85%)
- **Questions generated**: ~4,900
- **Seeds per generator**: 100 (0-99)
- **Total file size**: ~10-12 MB
- **Build time**: 2-3 minutes

### Error Handling

Some generators may fail due to:
- Missing `as_percent` attribute on Integer objects
- Division by zero in certain seeds
- Validation errors in teachers module

The build continues despite individual failures, generating questions for working seeds.

## JSON Structure

### Question Format

```json
{
  "beacon": "[1ere][sujets0][spé][sujet-1][automatismes][question-1]",
  "statement": "Quel est l'inverse du quintuple de $7$ ?",
  "answer": {
    "latex": "\\dfrac{1}{5 \\times 7}",
    "simplified_latex": "\\dfrac{1}{35}",
    "sympy_exp_data": {
      "type": "Rational",
      "sp.srepr": "Rational(1, 35)",
      "str": "1/35"
    },
    "formal_repr": "Fraction(p=Integer(n=1), q=Mul(l=Integer(n=5), r=Integer(n=7)))"
  },
  "components": {
    "n": "5",
    "x": "7"
  },
  "seed": 0,
  "generator": "spe_sujet1_auto_01_question"
}
```

### Index Format

```json
{
  "generators": [
    {
      "name": "spe_sujet1_auto_01_question",
      "file": "spe_sujet1_auto_01_question.py",
      "questions": [0, 1, 2, ...],  // Available seeds
      "successful": 100,
      "failed": 0
    }
  ],
  "total_questions": 4874,
  "seeds_per_generator": 100
}
```

## Routes & Templates

### Route: `/sujets0/ex-ante-generated`

**File**: `src/sujets0/router.py`

```python
@sujets0_router.get("/sujets0/ex-ante-generated", response_class=HTMLResponse)
async def sujets0_ex_ante_generated(request: Request):
    """
    Pre-generated questions viewer - Displays questions from the build process.
    """
```

**Features**:
- Loads index from `static/sujets0/questions/index.json`
- Displays statistics and generator cards
- Allows random question selection
- No Python execution required

### Template: `ex_ante_generated.html`

**File**: `src/templates/sujets0/ex_ante_generated.html`

**Features**:
- Generator grid with success/failure counts
- Random question loader
- Math rendering with KaTeX
- Expandable component details
- Smooth scrolling to selected questions

## JavaScript API

### Loading Questions

```javascript
// Load a random question from a generator
async function loadRandomQuestion(generatorName, maxSeed) {
    const seed = Math.floor(Math.random() * maxSeed);
    const url = `/static/sujets0/questions/${generatorName}/${seed}.json`;
    const response = await fetch(url);
    const question = await response.json();
    // Display question...
}

// Load a specific question by seed
async function loadSpecificQuestion(generatorName, seed) {
    const url = `/static/sujets0/questions/${generatorName}/${seed}.json`;
    const response = await fetch(url);
    return response.json();
}
```

## Comparison: Live vs Pre-Generated

| Aspect | Live Generation (`/sujets0`) | Pre-Generated (`/sujets0/ex-ante-generated`) |
|--------|------------------------------|-----------------------------------------------|
| **Load Time** | 5-10 seconds (Pyodide init) | Instant (<100ms) |
| **Dependencies** | Nagini, Pyodide, Teachers | None (just JSON) |
| **Browser Support** | Modern browsers only | All browsers |
| **Offline** | Requires CDN access | Works offline |
| **Flexibility** | Any seed, live editing | Fixed 100 seeds |
| **File Size** | 0 MB (generated on demand) | ~10 MB JSON |
| **Validation** | Runtime errors possible | Pre-validated |
| **Caching** | Not cacheable | Browser cacheable |

## Integration with Build Pipeline

### Manual Build

```bash
# Run whenever generators are updated
python src/build_questions.py
```

### Automatic Build on Startup

Add to `src/app.py` in the `lifespan` function:

```python
from src.build_questions import build_all_questions

async def lifespan(app: FastAPI):
    # ... existing startup code ...
    
    # Build questions if needed
    questions_dir = settings.base_dir / "src" / "static" / "sujets0" / "questions"
    if not questions_dir.exists() or settings.rebuild_questions:
        logger.info("Building pre-generated questions...")
        build_all_questions()
```

### GitHub Actions Build

```yaml
# .github/workflows/build.yml
- name: Generate Questions
  run: |
    python src/build_questions.py
    
- name: Upload Questions
  uses: actions/upload-artifact@v3
  with:
    name: questions
    path: src/static/sujets0/questions/
```

## Troubleshooting

### Common Issues

1. **"Questions not yet generated" error**
   - Run `python src/build_questions.py`
   - Check if `src/static/sujets0/questions/` exists

2. **Missing generators**
   - Some generators have errors (check build output)
   - ~16 generators have partial failures but still produce questions

3. **Math not rendering**
   - KaTeX CDN may be blocked
   - Check browser console for errors

4. **Question not loading**
   - Check if the seed exists for that generator
   - Use a seed within the `successful` count range

### Debugging

```bash
# Check build results
cat src/static/sujets0/questions/index.json | python -m json.tool | head -50

# Count total questions
find src/static/sujets0/questions -name "*.json" | wc -l

# Check specific generator
ls -la src/static/sujets0/questions/spe_sujet1_auto_01_question/

# View specific question
cat src/static/sujets0/questions/spe_sujet1_auto_01_question/0.json | python -m json.tool
```

## Future Improvements

1. **Incremental builds** - Only rebuild changed generators
2. **Seed expansion** - Generate more than 100 seeds if needed
3. **Question search** - Full-text search across all questions
4. **Export formats** - PDF, LaTeX, Word document generation
5. **Question filtering** - By difficulty, topic, type
6. **Analytics** - Track which questions are viewed most
7. **Error recovery** - Retry failed generators with different parameters
8. **Compression** - Gzip JSON files for smaller downloads

## Security Considerations

- JSON files are static and safe (no code execution)
- Questions are validated at build time
- No user input is executed
- LaTeX is rendered client-side by KaTeX (safe)
- All content is pre-generated and reviewed

## Performance Metrics

- **Initial page load**: <500ms
- **Question fetch**: <50ms
- **Math rendering**: <100ms
- **Total time to display**: <200ms
- **Bandwidth per question**: ~1-2 KB

Compare to live generation:
- **Pyodide init**: 5-10 seconds
- **Package loading**: 2-3 seconds
- **Generation**: 100-500ms
- **Total**: 7-14 seconds

**Performance improvement**: 35-70x faster
