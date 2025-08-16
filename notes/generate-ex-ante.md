






### Generate questions 

> This if for static analysis and ensuring 100% reproducibility and success. 

```bash
rm -rf src/static/sujets0/questions/

# Run build with seed injection
python src/build_questions.py --force-seed-injection

# Verify randomization
python -c "
import json
from pathlib import Path
# Check if different seeds produce different results
for gen in Path('src/static/sujets0/questions').iterdir():
    if gen.is_dir():
        q0 = json.load(open(gen / '0.json'))
        q1 = json.load(open(gen / '1.json'))
        if q0.get('statement') == q1.get('statement'):
            print(f'⚠️ {gen.name}: No variation detected')
"
```