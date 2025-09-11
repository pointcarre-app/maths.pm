


## High 


- UX : add button go back top for after generation page

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