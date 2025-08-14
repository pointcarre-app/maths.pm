---
title: Layout directive example (two columns)
---

# Layout directive example

This page demonstrates a two-column layout starting at the `sm` breakpoint using the layout directive.

## Two columns (>sm) with paragraph + SVG

--- {: .pm-cols-sm-2 gap-6 }

On a représenté la Corse sur la carte ci-dessous. Cette carte est en $2$ dimensions, elle est représentée sur une surface plane ($=$ "à plat"). On superpose un quadrillage assez particulier sur la carte.

![Carte de la Corse](/static/pm/corsica/files/corsica_grid_with_grid.svg)
{: .max-w-[500px] .mx-auto}

---

## Two columns with custom percentages (30/70)

--- {: .pm-cols-md-2 gap-4 .cols-30-70 }

Texte colonne 1 (30%).

![Carte de la Corse](/static/pm/corsica/files/corsica_grid_with_labels.svg)
{: .max-w-[600px] .mx-auto}

---

## Three columns (>md) variant (equal)

--- {: .pm-cols-md-3 gap-4 }

Colonne 1: texte de démonstration.

Colonne 2: texte de démonstration.

Colonne 3: texte de démonstration.

---

## Three columns with custom percentages (25/50/25)

--- {: .pm-cols-lg-3 gap-6 .cols-25-50-25 }

Texte 1 (25%).

![Carte de la Corse](/static/pm/corsica/files/corsica_with_grid.svg)
{: .max-w-[640px] .mx-auto}

Texte 3 (25%).

---

## Mixed fragments: paragraph + radios in columns

--- {: .pm-cols-sm-2 gap-5 .cols-60-40 }

Choisissez la bonne affirmation concernant les axes de la grille.

- Latitude {:20 | La latitude correspond à une ordonnée fixée (ligne horizontale).}
- Longitude {:21 | La longitude correspond à une abscisse fixée (ligne verticale).}
{: .i-radio}

![Carte de la Corse](/static/pm/corsica/files/corsica_grid_simple_no_title.svg)
{: .max-w-[420px] .mx-auto}

---

## Two columns (text | SVG) with tighter gap

--- {: .pm-cols-sm-2 gap-3 }

Quelques définitions et rappels utiles avant de lire la carte.
{: .pm-self-center }

![Carte de la Corse](/static/pm/corsica/files/corsica_no_grid.svg)
{: .max-w-[520px] .mx-auto}

---

## Two columns (SVG | radios) 50/50

--- {: .pm-cols-md-2 gap-6 .cols-50-50 }

![Carte de la Corse](/static/pm/corsica/files/corsica_grid_with_grid.svg)
{: .max-w-[560px] .mx-auto}

- Les lignes horizontales correspondent à
  - des latitudes {:20 | Bonne réponse}
  - des longitudes {:21 | Faux}
{: .i-radio}

---

## Two columns (text | radios) 40/60

--- {: .pm-cols-md-2 gap-5 .cols-40-60 }

Repérez l'affirmation correcte.
{: .pm-self-center }

- La longitude est une ordonnée fixée {:21 | Faux}
- La latitude est une ordonnée fixée {:20 | Correct}
{: .i-radio}

---

