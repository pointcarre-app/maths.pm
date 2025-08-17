# Mapping des Générateurs aux Compétences - Sujets 0

Ce document présente le mapping détaillé entre les fichiers générateurs de questions et les compétences du référentiel BAC 1ère.

## Vue d'ensemble

Les générateurs de questions sont organisés en deux catégories principales :
- **SPE Sujet 1** : 12 générateurs (`spe_sujet1_auto_01_question.py` à `spe_sujet1_auto_12_question.py`)
- **SPE Sujet 2** : 12 générateurs (`spe_sujet2_auto_01_question.py` à `spe_sujet2_auto_12_question.py`)

Chaque générateur est mappé à une ou plusieurs compétences du référentiel `bac_1_auto_1_1ERE` à `bac_1_auto_41_1ERE`.

## Dictionnaire de Mapping des Fichiers aux Compétences

### SPE Sujet 1

```python
{
    "spe_sujet1_auto_01_question.py": ["bac_1_auto_2_1ERE", "bac_1_auto_4_1ERE", "bac_1_auto_8_1ERE"],
    "spe_sujet1_auto_02_question.py": ["bac_1_auto_2_1ERE", "bac_1_auto_8_1ERE", "bac_1_auto_12_1ERE"],
    "spe_sujet1_auto_03_question.py": ["bac_1_auto_17_1ERE", "bac_1_auto_19_1ERE"],
    "spe_sujet1_auto_04_question.py": ["bac_1_auto_17_1ERE", "bac_1_auto_18_1ERE", "bac_1_auto_19_1ERE", "bac_1_auto_20_1ERE"],
    "spe_sujet1_auto_05_question.py": ["bac_1_auto_36_1ERE", "bac_1_auto_37_1ERE", "bac_1_auto_38_1ERE"],
    "spe_sujet1_auto_06_question.py": ["bac_1_auto_8_1ERE", "bac_1_auto_9_1ERE", "bac_1_auto_11_1ERE"],
    "spe_sujet1_auto_07_question.py": ["bac_1_auto_10_1ERE", "bac_1_auto_14_1ERE"],
    "spe_sujet1_auto_08_question.py": ["bac_1_auto_24_1ERE", "bac_1_auto_28_1ERE"],
    "spe_sujet1_auto_09_question.py": ["bac_1_auto_1_1ERE", "bac_1_auto_9_1ERE", "bac_1_auto_24_1ERE"],
    "spe_sujet1_auto_10_question.py": ["bac_1_auto_23_1ERE", "bac_1_auto_24_1ERE"],
    "spe_sujet1_auto_11_question.py": ["bac_1_auto_22_1ERE", "bac_1_auto_26_1ERE"],
    "spe_sujet1_auto_12_question.py": ["bac_1_auto_11_1ERE", "bac_1_auto_31_1ERE"]
}
```

### SPE Sujet 2

```python
{
    "spe_sujet2_auto_01_question.py": ["bac_1_auto_40_1ERE", "bac_1_auto_41_1ERE"],
    "spe_sujet2_auto_02_question.py": ["bac_1_auto_17_1ERE", "bac_1_auto_18_1ERE", "bac_1_auto_19_1ERE"],
    "spe_sujet2_auto_03_question.py": ["bac_1_auto_17_1ERE", "bac_1_auto_18_1ERE", "bac_1_auto_19_1ERE", "bac_1_auto_20_1ERE"],
    "spe_sujet2_auto_04_question.py": ["bac_1_auto_15_1ERE", "bac_1_auto_16_1ERE", "bac_1_auto_40_1ERE"],
    "spe_sujet2_auto_05_question.py": ["bac_1_auto_3_1ERE", "bac_1_auto_9_1ERE"],
    "spe_sujet2_auto_06_question.py": ["bac_1_auto_3_1ERE", "bac_1_auto_4_1ERE", "bac_1_auto_7_1ERE"],
    "spe_sujet2_auto_07_question.py": ["bac_1_auto_29_1ERE"],
    "spe_sujet2_auto_08_question.py": ["bac_1_auto_23_1ERE", "bac_1_auto_24_1ERE", "bac_1_auto_28_1ERE"],
    "spe_sujet2_auto_09_question.py": ["bac_1_auto_10_1ERE"],
    "spe_sujet2_auto_10_question.py": ["bac_1_auto_14_1ERE", "bac_1_auto_26_1ERE"],
    "spe_sujet2_auto_11_question.py": ["bac_1_auto_9_1ERE"],
    "spe_sujet2_auto_12_question.py": ["bac_1_auto_11_1ERE"]
}
```

## Justification Détaillée

### SPE Sujet 1

#### 1. `spe_sujet1_auto_01_question.py`
**Résumé** : Calculer l'inverse d'un multiple d'un nombre (ex. : inverse du quintuple de 7, soit 1/(5*7)).

**Compétences assignées** :
- `bac_1_auto_2_1ERE` : Implique des opérations sur fractions simples (multiplication et inverse).
- `bac_1_auto_4_1ERE` : Passer d'une expression à une forme fractionnaire simplifiée.
- `bac_1_auto_8_1ERE` : Calcul littéral élémentaire avec fractions et multiplicatives (ex. : 1/(n*x)).

**Pourquoi ?** La question teste des opérations basiques sur fractions et leur simplification, alignées sur les règles multiplicatives.

#### 2. `spe_sujet1_auto_02_question.py`
**Résumé** : Évaluer F = a + b/(c*d) avec fractions (incluant négatives).

**Compétences assignées** :
- `bac_1_auto_2_1ERE` : Opérations et comparaisons sur fractions (addition, division).
- `bac_1_auto_8_1ERE` : Calcul littéral avec expressions multiplicatives et additives (incluant négatifs).
- `bac_1_auto_12_1ERE` : Application numérique d'une formule algébrique.

**Pourquoi ?** C'est une évaluation directe d'une formule avec fractions complexes, nécessitant des opérations littérales et numériques.

#### 3. `spe_sujet1_auto_03_question.py`
**Résumé** : Prix multiplié par un coefficient, trouver le pourcentage d'augmentation/diminution.

**Compétences assignées** :
- `bac_1_auto_17_1ERE` : Conversion additive/multiplicative pour évolutions.
- `bac_1_auto_19_1ERE` : Calculer et exprimer un taux d'évolution en pourcentage.

**Pourquoi ?** C'est un cas simple de calcul de taux à partir d'un coefficient multiplicatif, avec expression en %.

#### 4. `spe_sujet1_auto_04_question.py`
**Résumé** : Augmentation puis diminution d'un prix par p%, calculer le pourcentage global de variation.

**Compétences assignées** :
- `bac_1_auto_17_1ERE` : Passer d'additif ("augmente de p%") à multiplicatif (multiplier par 1 + p/100).
- `bac_1_auto_18_1ERE` : Appliquer un taux d'évolution pour valeur finale.
- `bac_1_auto_19_1ERE` : Calculer un taux d'évolution en pourcentage.
- `bac_1_auto_20_1ERE` : Taux équivalent à évolutions successives.

**Pourquoi ?** La question porte sur des évolutions successives et leur taux global, cœur des compétences en variations.

#### 5. `spe_sujet1_auto_05_question.py`
**Résumé** : Probabilités de 3 faces d'un dé données, trouver la 4e pour que la somme soit 1.

**Compétences assignées** :
- `bac_1_auto_36_1ERE` : Probabilité entre 0 et 1.
- `bac_1_auto_37_1ERE` : Probabilité de l'événement contraire (x = 1 - somme des autres).
- `bac_1_auto_38_1ERE` : Probabilité comme somme des issues.

**Pourquoi ?** La question utilise la propriété que la somme des probabilités = 1, avec calcul de contraire et somme.

#### 6. `spe_sujet1_auto_06_question.py`
**Résumé** : Résoudre 1/x + 1/y = 1/u pour u en fonction de x et y.

**Compétences assignées** :
- `bac_1_auto_8_1ERE` : Calcul littéral avec fractions et additives/multiplicatives.
- `bac_1_auto_9_1ERE` : Réduire une expression algébrique.
- `bac_1_auto_11_1ERE` : Isoler une variable dans une égalité.

**Pourquoi ?** C'est un exercice classique d'isolation de variable avec manipulation de fractions.

#### 7. `spe_sujet1_auto_07_question.py`
**Résumé** : Résoudre x² > n comme inéquations du 1er degré (x > √n ou x < -√n).

**Compétences assignées** :
- `bac_1_auto_10_1ERE` : Résoudre x² = a.
- `bac_1_auto_14_1ERE` : Déterminer le signe d'une expression du second degré.

**Pourquoi ?** Transforme une inéquation quadratique en signes du 1er degré via racines.

#### 8. `spe_sujet1_auto_08_question.py`
**Résumé** : Donner l'équation y = ax + b d'une droite à partir d'un graphique.

**Compétences assignées** :
- `bac_1_auto_24_1ERE` : Reconnaître une fonction affine et sa représentation droite.
- `bac_1_auto_28_1ERE` : Lire graphiquement l'équation réduite d'une droite.

**Pourquoi ?** Directement lié à la lecture graphique d'équations linéaires.

#### 9. `spe_sujet1_auto_09_question.py`
**Résumé** : Identifier fonctions affines parmi expressions, trouver le coefficient directeur de plus grande valeur absolue.

**Compétences assignées** :
- `bac_1_auto_1_1ERE` : Comparer des nombres (valeurs absolues des coefficients).
- `bac_1_auto_9_1ERE` : Développer/réduire expressions pour vérifier si affines.
- `bac_1_auto_24_1ERE` : Reconnaître fonctions affines.

**Pourquoi ?** Nécessite réduction d'expressions et comparaison de slopes.

#### 10. `spe_sujet1_auto_10_question.py`
**Résumé** : Donner équation de parabole ax² + c (|a|=1) à partir d'un graphique.

**Compétences assignées** :
- `bac_1_auto_23_1ERE` : Exploiter une équation de courbe (appartenance, coordonnées).
- `bac_1_auto_24_1ERE` : Reconnaître forme quadratique (extension d'affine).

**Pourquoi ?** Implique lecture graphique et exploitation d'équation quadratique.

#### 11. `spe_sujet1_auto_11_question.py`
**Résumé** : À partir d'un graphique de fonction, déterminer le signe de x * f(x) à un point.

**Compétences assignées** :
- `bac_1_auto_22_1ERE` : Déterminer images/antécédents graphiquement.
- `bac_1_auto_26_1ERE` : Déterminer signe d'une fonction graphiquement.

**Pourquoi ?** Teste l'analyse du signe d'une expression via graphique.

#### 12. `spe_sujet1_auto_12_question.py`
**Résumé** : Trouver un coefficient pour obtenir une moyenne pondérée donnée.

**Compétences assignées** :
- `bac_1_auto_11_1ERE` : Isoler variable dans formule de moyenne.
- `bac_1_auto_31_1ERE` : Calculer et interpréter une moyenne.

**Pourquoi ?** C'est un calcul de moyenne pondérée avec isolation de variable.

### SPE Sujet 2

#### 1. `spe_sujet2_auto_01_question.py`
**Résumé** : À partir d'un arbre de probabilités, calculer P(B) en utilisant des probabilités conditionnelles (P(B|A) et P(B|¬A)).

**Compétences assignées** :
- `bac_1_auto_40_1ERE` : Calculer des probabilités conditionnelles à partir d'un arbre pondéré.
- `bac_1_auto_41_1ERE` : Distinguer P(A ∩ B), P_A(B), P_B(A) (ici, via loi des probabilités totales).

**Pourquoi ?** La question implique un calcul conditionnel classique avec arbre, distinguant intersections et conditionnelles.

#### 2. `spe_sujet2_auto_02_question.py`
**Résumé** : Prix initial, diminution de p%, calculer le nouveau prix.

**Compétences assignées** :
- `bac_1_auto_17_1ERE` : Passer d'additif ("diminue de p%") à multiplicatif (multiplier par 1 - p/100).
- `bac_1_auto_18_1ERE` : Appliquer un taux d'évolution pour valeur finale.
- `bac_1_auto_19_1ERE` : Calculer un taux d'évolution (implicite dans la conversion).

**Pourquoi ?** C'est un calcul direct d'évolution unique, avec conversion additive/multiplicative.

#### 3. `spe_sujet2_auto_03_question.py`
**Résumé** : Augmentation puis diminution d'un prix par p%, calculer le pourcentage global de variation (identique à un fichier de sujet1).

**Compétences assignées** :
- `bac_1_auto_17_1ERE` : Conversion additive/multiplicative pour évolutions.
- `bac_1_auto_18_1ERE` : Appliquer taux pour valeur finale.
- `bac_1_auto_19_1ERE` : Calculer taux d'évolution en %.
- `bac_1_auto_20_1ERE` : Taux équivalent à évolutions successives.

**Pourquoi ?** Identique à un cas précédent ; focus sur évolutions composées et taux global.

#### 4. `spe_sujet2_auto_04_question.py`
**Résumé** : Proportion d'internes, proportion de gauchers parmi eux, calculer pourcentage global de gauchers internes.

**Compétences assignées** :
- `bac_1_auto_15_1ERE` : Calculer et exprimer une proportion en pourcentage.
- `bac_1_auto_16_1ERE` : Utiliser proportion pour calculer partie/tout.
- `bac_1_auto_40_1ERE` : Probabilités conditionnelles (ici, comme proportions : P(gaucher|interne) * P(interne)).

**Pourquoi ?** C'est un calcul de proportion composée, analogue à une probabilité conditionnelle.

#### 5. `spe_sujet2_auto_05_question.py`
**Résumé** : Simplifier fraction avec puissances (ex. : 6^14 / 3^5) en gardant facteurs premiers.

**Compétences assignées** :
- `bac_1_auto_3_1ERE` : Opérations sur puissances (division, exposants).
- `bac_1_auto_9_1ERE` : Réduire expression algébrique (factorisation en primes).

**Pourquoi ?** Manipulation d'exposants et simplification en facteurs premiers.

#### 6. `spe_sujet2_auto_06_question.py`
**Résumé** : Convertir énergie de Joules à kWh avec facteur donné (puissances de 10).

**Compétences assignées** :
- `bac_1_auto_3_1ERE` : Opérations sur puissances (division avec exposants).
- `bac_1_auto_4_1ERE` : Passer d'une écriture décimale/fractionnaire.
- `bac_1_auto_7_1ERE` : Conversions d'unités (énergie : J à kWh).

**Pourquoi ?** Implique manipulation de puissances et conversion d'unités avec arrondi.

#### 7. `spe_sujet2_auto_07_question.py`
**Résumé** : Calculer coefficient directeur d'une droite passant par deux points.

**Compétences assignées** :
- `bac_1_auto_29_1ERE` : Déterminer coefficient directeur à partir de coordonnées de deux points.

**Pourquoi ?** Calcul direct de slope = (y2 - y1)/(x2 - x1), cœur de cette compétence.

#### 8. `spe_sujet2_auto_08_question.py`
**Résumé** : Équation de droite en forme ax + by + c = 0, avec |slope| = 1, à partir d'un graphique.

**Compétences assignées** :
- `bac_1_auto_23_1ERE` : Exploiter équation de courbe (calcul coordonnées).
- `bac_1_auto_24_1ERE` : Reconnaître fonction affine et sa forme.
- `bac_1_auto_28_1ERE` : Lire graphiquement l'équation réduite.

**Pourquoi ?** Nécessite lecture graphique et conversion à forme générale.

#### 9. `spe_sujet2_auto_09_question.py`
**Résumé** : Résoudre x² = n sur les réels (trouver ±√n).

**Compétences assignées** :
- `bac_1_auto_10_1ERE` : Résoudre équation du type x² = a.

**Pourquoi ?** C'est exactement cette forme d'équation quadratique simple.

#### 10. `spe_sujet2_auto_10_question.py`
**Résumé** : Déterminer signe d'une fonction quadratique f(x) = (a1x + b1)(a2x + b2) sur un intervalle donné.

**Compétences assignées** :
- `bac_1_auto_14_1ERE` : Déterminer signe d'expression factorisée du second degré.
- `bac_1_auto_26_1ERE` : Déterminer signe d'une fonction (ici algébriquement, sans graphique explicite).

**Pourquoi ?** Analyse de signe via racines et coefficients, pour un intervalle spécifique.

#### 11. `spe_sujet2_auto_11_question.py`
**Résumé** : Développer (x + a)^2.

**Compétences assignées** :
- `bac_1_auto_9_1ERE` : Développer expression algébrique simple (identité remarquable (a+b)^2).

**Pourquoi ?** Application directe de l'identité de développement.

#### 12. `spe_sujet2_auto_12_question.py`
**Résumé** : Résoudre v en fonction de a et R dans a = v² / R.

**Compétences assignées** :
- `bac_1_auto_11_1ERE` : Isoler une variable dans une égalité (v = √(a R)).

**Pourquoi ?** Isolation simple de v avec racine carrée.

## Statistiques de Répartition

### Compétences les plus utilisées :
- `bac_1_auto_17_1ERE`, `bac_1_auto_18_1ERE`, `bac_1_auto_19_1ERE` : Évolutions et pourcentages (6 occurrences)
- `bac_1_auto_9_1ERE` : Calcul algébrique (4 occurrences)
- `bac_1_auto_11_1ERE` : Isolation de variables (3 occurrences)
- `bac_1_auto_24_1ERE` : Fonctions affines (4 occurrences)

### Domaines couverts :
- **Calcul numérique** : Fractions, puissances, pourcentages
- **Calcul algébrique** : Développement, factorisation, résolution
- **Fonctions** : Affines, quadratiques, lecture graphique
- **Probabilités** : Calculs conditionnels, événements
- **Géométrie analytique** : Équations de droites
- **Statistiques** : Moyennes, proportions

---

*Ce mapping a été établi par analyse du code des générateurs et des compétences du référentiel BAC 1ère.*
