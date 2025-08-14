---
chapter_rdb: Bases du langage Python
---

[TOC]

# 👣 Premiers pas avec Python

Ces premiers pas ne deviendront pas une chorégraphie virale, mais ils t'apprendront quelque chose. Bref, tout l'opposé de Tiktok.
{: .lead}

![](/images/computer-desk-old-169.jpg)

## 📺 Affichages avec la fonction `print`

Lorsque l'on code, tout se passe à l'intérieur de la machine. On a donc besoin d'indiquer au programme si l'on souhaite qu'il affiche des valeurs à l'écran. En Python, c'est la fonction `print` qui permet de réaliser un affichage.

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

## 🧪 Démo des fragments (couverture complète)

---

### Listes simples

- Premier élément
- Deuxième élément

1. Étape 1
2. Étape 2

### Liste labellisée

<ul>
  <li class="lbl">Définition</li>
  <li class="lbl">Théorème</li>
  <li class="lbl">Exemple</li>
  <li class="lbl">Remarque</li>
  <li class="lbl">Conclusion</li>
</ul>

### Question à choix (radio)

<ul>
  <li class="i-radio">Paris{: 0}</li>
  <li class="i-radio">Ajaccio{: 1}</li>
  <li class="i-radio">Lyon{: 0}</li>
</ul>

### Tableau

| Nom | Valeur |
|---|---|
| a | 1 |
| b | 2 |

### Séparateur

---

### Vector graph (HTML)

```html
<vector-graph width="300" height="200"></vector-graph>
```

### Graph (YAML)

```yaml
graphPCAVersion: 1
title: "Graphe d'exemple"
```

### Table de variations (YAML avec classe)

```yaml {.table-variations}
headers: [x, f(x)]
rows:
  - [-2, 5]
  - [0, 1]
  - [2, -3]
```
