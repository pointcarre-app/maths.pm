# 🚀 Quick Start: Pre-Generated Questions

## What is it?

A system that pre-generates ~5000 math questions as JSON files for instant loading, without needing Python in the browser.

## How to Use

### 1. Generate Questions (One-time setup)

```bash
# Run this after cloning or when generators change
python src/build_questions.py

# Takes 2-3 minutes, generates ~5000 questions
```

### 2. Access the Viewer

```bash
# Start the server
python -m src.app

# Visit in browser
http://localhost:5001/sujets0/ex-ante-generated
```

### 3. View Questions

- Click "Voir une question" on any generator card
- Questions load instantly (no Python execution)
- Math is rendered with KaTeX

## Key URLs

| URL | Description |
|-----|-------------|
| `/sujets0` | Live generation with Nagini (slow, flexible) |
| `/sujets0/ex-ante-generated` | Pre-generated viewer (instant) |
| `/scenery` | Testing environment |

## File Locations

```
src/
├── build_questions.py           # Run this to generate
└── static/sujets0/questions/   # Generated JSON files (5000+)
    ├── index.json              # Master index
    └── [generator_name]/       # 100 questions per generator
        └── 0-99.json          # Individual questions
```

## Example Question JSON

```json
{
  "statement": "Quel est l'inverse du quintuple de 7 ?",
  "answer": {
    "simplified_latex": "\\dfrac{1}{35}"
  },
  "seed": 0,
  "generator": "spe_sujet1_auto_01_question"
}
```

## Benefits

✅ **Instant loading** - No 10-second wait for Pyodide  
✅ **Works offline** - JSON files are cached  
✅ **All browsers** - No modern JavaScript required  
✅ **Pre-validated** - Errors caught at build time  
✅ **Reproducible** - Same seed = same question  

## When to Rebuild

Rebuild questions when:
- Generator files (`.py`) are modified
- New generators are added
- You want different random seeds

```bash
# Quick rebuild command
cd /path/to/project && python src/build_questions.py
```

## Troubleshooting

**"Questions not yet generated"**
→ Run `python src/build_questions.py`

**Math not rendering**
→ KaTeX CDN may be blocked, check console

**Generator missing**
→ Some generators have errors, check build output

## API Usage

```javascript
// Fetch any question directly
fetch('/static/sujets0/questions/spe_sujet1_auto_01_question/42.json')
  .then(r => r.json())
  .then(q => console.log(q.statement));
```

## Statistics

- **Build time**: 2-3 minutes
- **Questions generated**: ~4,900
- **Storage used**: ~10 MB
- **Load time**: <200ms (vs 10+ seconds for live)
- **Success rate**: 85% of generators work
