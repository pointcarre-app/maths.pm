
## High


- [] Ensure `random.seed` is used in all the generators


- [] Every domain / product yaml should have his own validation rules (using online mode to ensure hosted versions exists)


- [ ] Seed from the form but need 100% lvl of certainty of reproducibility (careful random.seed in generators (or done above already ? ))


### Sujets 0 

- []  Correct the level for the questions in generators. (should be done in the yaml sujets0 )

- [] Proposer une sélection manuelle par générateur (par filière)


- [] Add non sorted function with same generators (ie position of generator in final sheet will be random)

- [] document the fact we adapted the stuff for the maths answer instead of MCQ


- [] Add in form possibility of adding cluz + big clue (ie video)

- [] considérer sélection sur le niveau + mode MCQ 

- [] spe_sujet1_auto_06_question.py: make better for equiv relation de conjugaisons avec coeff entiers relatifs


# TODO Sel:
- [] spe_sujet1_auto_03_question.py :  
> "Le prix d'un article est multiplié par `${coef.latex().replace('.', ',')}$`. Calculer la variation relative $V_r$ de ce prix.
Donc il faut proposer un corrigé: 
- qui invoque avec simplicité ce qu'est la variation relative: ie la hausse ou la baisse en pourcentage par rapport à la valeur initiale: ie 0.86 = (1-14)/100 = 14% de baisse Donc $V_r = 0.86
- la méthode full calcul: on pose le prix $p$ et $v_r=\dfrac{p -0.86p}{p} = 0.14$ donc $V_r = 0.14 = 14\\%$
- La méthode last resort : tu peux prendre un prix de 100 et faire le calcul, ça marchera (monde linéaire)
- $V_r=\dfrac{100 - 86}{100} = 0.14 = 14\\%$

### For Teachers


- Extract and finish hypercube (for fork v4.py.js from fork vector_graph)

## Corsica

- [ ]  Latex or at least repositionn 10km 10km on square svg


- [ ] Ensure Open Sourcing of all the products ☔️





- [] for AGPL compliance: extract the 3RD-PARTY-LICENSES.md file from the repo by http request at building step
- [] therefore you need to normalize format at least for the table


- [] then ensure you do it also for each product



## Generic

- [ ] Rule should be one view per router then use only core pm/...



- [ ] Add a layer of template for eveery index page not to repete the config and metatags
    - [ ] Ensure layer present but dont supercede the ones from the markdowns



## DaisyUI root adapter

```css
--color-primary-ghost: color-mix(in oklab, var(--color-primary, var(--color-base-content)) 8%, var(--color-base-100));

--color-secondary-ghost: color-mix(in oklab, var(--color-secondary, var(--color-base-content)) 8%, var(--color-base-100));

--color-accent-ghost: color-mix(in oklab, var(--color-accent, var(--color-base-content)) 8%, var(--color-base-100));

--color-base-content-ghost: color-mix(in oklab, var(--color-base-content, var(--color-base-content)) 8%, var(--color-base-100));
```


- [] should be -soft ? pretty sure










