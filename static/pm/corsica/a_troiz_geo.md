---
# chapter_rdb: Bases du langage Python
class_at_school: troiz
---

[TOC]



# Géographie de l'île

Ou comment apprendre à calculer une surface à partir d'une carte, simplement en dessinant de petits carrés. ▣
{: .pm-subtitle}

![Header](/static/pm/corsica/files/header.html)
{: .border-[0.1px] .border-primary/60 .card}



## 🔲 Quadrillage sur une surface plane

--- {: .pm-cols-sm-2 gap-3 .cols-60-40 .mt-6}

On a représenté la Corse sur la _Carte 1_. Cette carte est en $2$ dimensions (sur une surface plane).<br><br>On superpose un quadrillage assez particulier sur la carte, il s'agit du type de quadrillage qui sont (entre autres) sur les globes terrestres.<br><br>
**C'est grâce à ce quadrillage que tu vas pouvoir calculer la surface de la Corse.**
{: .pm-self-center}

![Carte 1](/static/pm/corsica/files/corsica_grid_with_grid.svg)
{: .mx-auto}

---

## 📏 Unités

Sur cette carte, les lignes horizontales de ce quadrillage sont des lignes de même :
{: .statement}

- Latitude {:20 | Sur une représentation plane, la latitude se lit verticalement, et correspond donc à une ligne horizontale.}
- Longitude {:21 | Sur une représentation plane, la longitude se lit horizontalement, et correspond donc à une ligne verticale.}
  {: .i-radio}

Tandis que les lignes verticales sont des lignes de même :
{: .statement}

- Latitude {:21 | Sur une représentation plane, la latitude se lit verticalement, et correspond donc à une ligne horizontale.}
- Longitude {:20 | Sur une représentation plane, la longitude se lit horizontalement, et correspond donc à une ligne verticale.}
- General Info{:29 | Un petit moyen mnémotechnique : les voyelles sont croisées : la l**A**titude est une **O**rdonnée, tandis que la l**O**ngitude est une **A**bscisse.}
  {: .i-radio}

Pour exprimer des latitudes et longitudes, on utilise des unités de mesure spécifiques :
{: .statement}

- Degrés, minutes et secondes {:20 | Exemple : ($41°55'0.02"$ $N$ ; $8°43'59.99"$ $E$) pour 41 degrés, 55 minutes et 0.02 secondes Nord, et 8 degrés, 43 minutes et 59.99 secondes Est.}
- Kilomètres {:21 | Non, car ces coordonnées ne sont pas appropriées aux géométriques sphériques, or la Terre est une sphère.}
  {: .i-radio}

## 📍 Coordonnées d'Ajaccio et Bastia


![Carte 2 : Corse, ports d'Ajaccio et Bastia](/static/pm/corsica/files/corsica_grid_with_cities.svg)
{: .max-w-[500px] .mx-auto}


Sur la _Carte 2_, on a représenté les positions des ports d'Ajaccio et Bastia avec deux points deux couleurs différentes. Sachant que les coordonnées des ports de ces deux villes sont :

| Port    | Latitude       | Longitude     |
| ------- | -------------- | ------------- |
| Ajaccio | $41°55'17"$ $N$ | $8°44'22"$ $E$ |
| Bastia  | $42°42'20"$ $N$ | $9°27'15"$ $E$ |



La couleur du bouton représente la couleur du point sur la carte. Parmi les 4 propositions ci-dessous, deux sont correctes, deux sont fausses. Clique sur une proposition correcte.
{: .statement}

- <div class="badge badge-secondary badge-xs" style="border-radius: 15rem;"></div> Ajaccio {:21 .btn-secondary .btn-outline}
- <div class="badge badge-secondary badge-xs" style="border-radius: 15rem;"></div> Bastia {:20 .btn-secondary .btn-outline}
- <div class="badge badge-accent badge-xs" style="border-radius: 15rem;"></div> Ajaccio {:20 .btn-accent .btn-outline}
- <div class="badge badge-accent badge-xs" style="border-radius: 15rem;"></div> Bastia {:21 .btn-accent .btn-outline}
- Ajaccio a la plus petite longitude et est donc plus à l'ouest que Bastia. Sa longitude est également plus petite que celle de Bastia, donc Ajaccio est plus au Sud. Donc le point <div class="badge badge-accent badge-xs" style="border-radius: 15rem;"></div> correspond à Ajaccio et le point <div class="badge badge-secondary badge-xs" style="border-radius: 15rem;"></div> correspond à Bastia. {:29}
{: .i-radio}




## 📏 Représentations des distances


Les conversions entre des données de latitude et longitude exprimées en degrés, minutes et secondes vers des distances en kilomètres sont assez complexes et dépassent largement le niveau troisième.
{: .alert .alert-info .alert-soft}


Nous nous sommes donc assurés de choisir un quadrillage qui tombe *"quasi-juste"* : chaque carré fait $10$ $km$ de côté.
{: .alert .alert-success .alert-soft}



![Carte 3 : Corse avec quadrillage $10$ $km$ par $10$ $km$](/static/pm/corsica/files/corsica_grid_square.svg)
{: .mx-auto}


💡 _Horitontalement, on compte 9 carrés, et verticalement 19 carrés._<br>
Quelle est la surface totale représentée sur cette carte ? Tu exprimeras ton résultat en $km^2$, arrondi à l'unité (c'est à dire, sans virgule).
{: .statement}






```yaml
NumberInputPCA: v0.0.1
id: total_surface
type: number
# label: "How many apples are in the basket?"
min: 0
max: 20000
step: 100
correct: 17100
unit: "$km^2$"
tolerance: 0
feedback_correct: "$19 \\times 9 \\ times 10$ $km$ $\\times 10$ $km$ = 17100"
feedback_incorrect: "Réponse incorrecte."
# hint: "They are arranged in 3 rows of 4 apples."
```




## 🧮 Calcul de la surface de l'île



![Carte 3 : Carte de la Corse avec quadrillage $10$ $km$ par $10$ $km$](/static/pm/corsica/files/corsica_grid_cells_dichotomy.svg)
{: .mx-auto}



- Il y a en tout $58$ carrés colorés <span class="badge badge-secondary badge-xs" style="border-radius: 15rem;"></span>.
- Il y a en tout $117$ carrés colorés <span class="badge badge-accent badge-xs" style="border-radius: 15rem;"></span>.
{: .alert .alert-info .alert-soft}





La surface colorée avec cette couleur <span class="badge badge-secondary badge-xs" style="border-radius: 15rem;"></span> correspond à la surface des carrés qui sont entièrement dans l'île. Calcule cette surface en $km^2$.
{: .statement}



```yaml
NumberInputPCA: v0.0.1
id: surface_within_the_island
type: number
# label: "How many apples are in the basket?"
min: 0
max: 20000
step: 100
correct: 5800
unit: "$km^2$"
tolerance: 0
feedback_correct: "$58 \\times 10$ $km$ $\\times 10$ $km$ = 5800 $km^2$"
feedback_incorrect: "Réponse incorrecte."
# hint: "They are arranged in 3 rows of 4 apples."
```



La surface colorée avec cette couleur <span class="badge badge-accent badge-xs" style="border-radius: 15rem;"></span> correspond à la surface des carrés qui sont partiellement dans l'île. Calcule la surface totale représentées par les carrées colorés <span class="badge badge-secondary badge-xs" style="border-radius: 15rem;"></span> et <span class="badge badge-accent badge-xs" style="border-radius: 15rem;"></span> en $km^2$.
{: .statement}



```yaml
NumberInputPCA: v0.0.1
id: surface_within_the_island
type: number
# label: "How many apples are in the basket?"
min: 0
max: 20000
step: 100
correct: 11700
unit: "$km^2$"
tolerance: 0
feedback_correct: "$117 \\times 10$ $km$ $\\times 10$ $km$ = 11700 $km^2$"
feedback_incorrect: "Réponse incorrecte."
# hint: "They are arranged in 3 rows of 4 apples."
```



## 🏘️ Notion de voisinage

🏗️ 🏗️ 🏗️ À paraître en 2026.
*Tu découvriras ici une façon encore plus maline de sélectionner les carrés que l'on inclut dans la surface de l'île, grâce à la notion de voisinage. Cette méthode permet d'être encore plus précis que ci-dessus*
{: .alert .alert-info .alert-soft .mt-12}





