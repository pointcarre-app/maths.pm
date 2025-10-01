


## High 

- [] Prepare possible backend interactions
     - [] Login
     - [] Store
     - [] Stats
     - [] Next


- []  Fix this for code_
     - [] Test
- [] Ensure it doesnt break "codex_" (CodeMirror should do some stuff on it's own)
     - [] Test (like with pandas &, | and also < and >)

```bash
brew update && brew install pyenv
```
Lead to amp & amp


see in `fragment_builder.py` : 


```python
# Convert values and handle HTML entities
for key, value in data.items():
     if isinstance(value, int):
          data[key] = str(value)
     elif isinstance(value, str):
          if "&gt;" in value:
               value = value.replace("&gt;", ">")
          if "&lt;" in value:
               value = value.replace("&lt;", "<")
          if "&amp;" in value:
               value = value.replace("&amp;", "&")
          data[key] = value

```


- [] UX : add button go back top for after generation page

- [] Seed injection is done for random in sujets0_question_generator_v1.js cf below
     - No need in generators .py files

- [] Migrate Doppel
     - Use case in `pca-mathspm/files/scripts/sujets0_question_generator.js` or `nagini.js` 
     ```js
             // Also random.Seed in some generators... TODO sel
        // seems better here only
        // Technically the same seed
        // But this doesnt run in doppel:backend..
        // so duplication for safety locally + ?? 
        // compare wiyh a new doppel


        // Inject seed
        const seedInjection = `\nimport random\nrandom.seed(${seed})\n\n# Override the default SEED\nimport teachers.defaults\nteachers.defaults.SEED = ${seed}\n\n`;
     ```



## Medium



- pm system:
     - Consider the case of the folders if scenario is static deployment

- dataviz2:
     - Pie plot GDP : colors and country names





## Low

```
    format: str = Query(
        "html", description="Response format (json or html)", pattern="^(json|html)$"
    ),
```

- pattern or regex ? both works ?