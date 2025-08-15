---
# chapter_rdb: Bases du langage Python
# Page-specific metatags
title: "Surface de la Corse avec Python - Statistiques et programmation"
description: "Apprenez Python en calculant la surface de la Corse. Introduction à la programmation et aux statistiques pour lycéens de seconde."
keywords: "python, corse, statistiques, programmation, seconde, lycée, surface, calcul, print, variables"
author: "Maths.pm - Équipe Python Corsica"
robots: "index, follow"
# Open Graph metatags
og:title: "Introduction à Python - Calcul de la surface de la Corse"
og:description: "Cours interactif de Python pour débutants : apprenez à programmer en calculant la surface de la Corse."
og:image: "https://maths.pm/images/computer-desk-old-169.jpg"
og:type: "article"
og:url: "https://maths.pm/pm/corsica/e_seconde_stats_python.md"
# Twitter Card metatags
twitter:card: "summary_large_image"
twitter:title: "Python & Géographie de la Corse"
twitter:description: "Apprenez Python en calculant des surfaces géographiques"
twitter:image: "https://maths.pm/images/computer-desk-old-169.jpg"
# Dublin Core metatags
DC.title: "Introduction à Python avec la géographie corse"
DC.creator: "Maths.pm Python Corsica"
DC.subject: "Programmation, Python, Géographie, Mathématiques"
DC.description: "Cours de programmation Python appliqué à la géographie"
# Additional metatags
abstract: "Introduction à la programmation Python à travers le calcul de surfaces géographiques"
topic: "Programmation Python et statistiques"
category: "Informatique, Mathématiques, Seconde"
revised: "2025-01-15"
pagename: "Python et surface de la Corse"
---

[TOC]

# 🏝️ Surface de l'île & introduction à Python

Apprendre à calculer une surface à partir d'une carte, avec Python
{: .lead}


Aucune connaissance préalable programmation ou concernant le langage Python n'est requise ☺
{: .alert .alert-info}

![](/images/computer-desk-old-169.jpg)

## 📺 Affichages avec la fonction `print`

Lorsque l'on code, tout se passe à l'intérieur de la machine. On a donc besoin d'indiquer au programme si l'on souhaite qu'il affiche des valeurs à l'écran. En Python, c'est la fonction `print` qui permet de réaliser un affichage.



Morceau de code pour passer des latitudes/longitudes en coordonnées cartésiennes / distances
Morceau de code qui va coloriser les carrés,  sur le svg
et morceau de code pour aire totale

```yaml
codexPCAVersion: 1
script_path: "pyly/premiers-pas-affichages-strings.py"
```

```yaml
codexPCAVersion: 1
script_path: "pyly/premiers-pas-affichages-integers.py"
```

## 🧮 Calculatrice

### Addition et soustraction avec `+` et `-`

### Multiplication et division `*` et `/`

```yaml
codexPCAVersion: 1
script_path: "pyly/premiers-pas-multiplications.py"
```

### Division euclidienne avec `//` et `%`

### Priorité des opérations

En utilisant la fonction `print`, calcule combien d'heures tu as passé à dormir si tu dors 8h par nuit depuis que t'es né (prends ton âge en années).
{: .bg-secondary}

> Si t'as 16 ans, tu devrais trouver 16 × 365 × 8 heures de sommeil. Ça fait un paquet d'heures sur TikTok manquées, non ? 😉

```yaml
codexPCAVersion: 1
script_path: "pyly/premiers-pas-multiplications.py"
```

## 📦 Variables

Comme en maths, tes boîtes préférées

Plutôt que de tout calculer d'un coup, on peut stocker des valeurs dans des variables. C'est comme créer des raccourcis !
{: .bg-white}

Par exemple :

```python
age = 16                  # Mon âge
jours_par_an = 365        # Nombre de jours dans une année
heures_dodo = 8           # Heures de sommeil par nuit
total = age * jours_par_an * heures_dodo
print("J'ai dormi environ", total, "heures dans ma vie !")
```

T'inquiète pas si tu comprends pas tout, on va y aller step by step.
{: .bg-white}

```yaml
codexPCAVersion: 1
script_path: "intro/variables_intro.py"
```

Crée des variables pour calculer combien de minutes tu passes sur ton téléphone en une année si tu y passes 3 heures par jour. Utilise des noms de variables qui ont du sens !
{: .bg-secondary}

> C'est souvent plus facile de décomposer un problème en plusieurs étapes avec des variables intermédiaires qu'essayer de tout faire en une seule ligne.

```yaml
codexPCAVersion: 1
script_path: "intro/variables_question_1.py"
```

## 💬 Commentaires

Soit $a$ un réel non nul. Calculer l'unique antécédent de $0$ par la fonction $f$ définie sur $\mathbb{R}$ par $f(x)=ax+b$.

```yaml
mathPCAVersion: 1
mask: x_0=
nature: give_formula
expression: -b/a
perfect_test: -\frac{b}{a}
```

## 🔁 Récap

<!-- # Variables et affichages

Pour découvrir ce langage de programmation, utilisons Python comme une calculatrice !
{: lead}

[TOC]

## Quelques calculs

- Blablablablabl
- Blablabla
  {: .bg-white .nm .li-mb-more }

```yaml
codexPCAVersion: 1
script_path: "intro/calculatrice_4_ope.py"
```

En utilisant la fonction `print`, et l'opérateur `+`, écris du code qui calcule le nombre de jours au cours de la décennie 2010-2019.
{: .bg-secondary}

(ca envoie le code)

> Lalal

```yaml
codexPCAVersion: 1
script_path: "intro/calculatrice_4_ope_question_0.py"
```

## Example maths for later

Soit $a$ un réel non nul. Calculer l'unique antécédent de $0$ par la fonction $f$ définie sur $\mathbb{R}$ par $f(x)=ax+b$.

```yaml
mathPCAVersion: 1
mask: x_0=
nature: give_formula
expression: -b/a
perfect_test: -\frac{b}{a}
``` -->



## 🟪 Découpage en carrés de côté $10$ km

![Carte 3 de la Corse](/static/pm/corsica/files/corsica_grid_with_grid.svg)
{: .mx-auto}

Calculs pour passer de longitude/lattitude dépassent niveau troisième, mais on peut utiliser une approximation qui fonctionne plutôt bien. Quelle échelle ?

![](/images/computer-desk-old-169.jpg)

## 📺 Affichages avec la fonction `print`

Lorsque l'on code, tout se passe à l'intérieur de la machine. On a donc besoin d'indiquer au programme si l'on souhaite qu'il affiche des valeurs à l'écran. En Python, c'est la fonction `print` qui permet de réaliser un affichage.

```yaml
codexPCAVersion: 1
script_path: "pyly/premiers-pas-affichages-strings.py"
```
