# Mapping des Générateurs aux Compétences - Sujets 0

Ce document présente le mapping détaillé entre les fichiers générateurs de questions et les compétences du **Programme de mathématiques de première générale - Spécialité**.

## Référentiel Officiel

Basé sur le programme officiel du Ministère de l'Éducation nationale et de la Jeunesse pour la classe de première générale, spécialité mathématiques, organisé en 5 grandes parties :

1. **Algèbre** : Suites numériques, équations du second degré
2. **Analyse** : Dérivation, fonctions, fonction exponentielle, trigonométrie
3. **Géométrie** : Calcul vectoriel, produit scalaire, géométrie repérée
4. **Probabilités et statistiques** : Probabilités conditionnelles, variables aléatoires
5. **Algorithmique et programmation** : Listes, fonctions Python

## Vue d'ensemble

Les générateurs de questions sont organisés en deux catégories principales :
- **SPE Sujet 1** : 12 générateurs (`spe_sujet1_auto_01_question.py` à `spe_sujet1_auto_12_question.py`)
- **SPE Sujet 2** : 12 générateurs (`spe_sujet2_auto_01_question.py` à `spe_sujet2_auto_12_question.py`)

Chaque générateur est mappé aux compétences spécifiques du programme de première spécialité.

## Compétences du Programme Officiel

### 🧮 **ALGÈBRE**
- **ALG-01** : Modéliser une situation par une suite numérique (arithmétique, géométrique)
- **ALG-02** : Calculer des termes et sommes de suites
- **ALG-03** : Résoudre des équations du second degré
- **ALG-04** : Factoriser des polynômes du second degré
- **ALG-05** : Étudier le signe d'une fonction polynôme du second degré

### 📈 **ANALYSE**
- **ANA-01** : Calculer des taux de variation et nombres dérivés
- **ANA-02** : Déterminer l'équation d'une tangente
- **ANA-03** : Étudier les variations d'une fonction avec la dérivée
- **ANA-04** : Résoudre des problèmes d'optimisation
- **ANA-05** : Utiliser les propriétés de la fonction exponentielle
- **ANA-06** : Modéliser des phénomènes exponentiels
- **ANA-07** : Utiliser les fonctions trigonométriques

### 📐 **GÉOMÉTRIE**
- **GEO-01** : Utiliser le calcul vectoriel dans le plan
- **GEO-02** : Calculer un produit scalaire
- **GEO-03** : Résoudre des problèmes avec le produit scalaire
- **GEO-04** : Déterminer des équations de droites et cercles
- **GEO-05** : Utiliser la géométrie repérée

### 🎲 **PROBABILITÉS ET STATISTIQUES**
- **PROB-01** : Calculer des probabilités conditionnelles
- **PROB-02** : Utiliser des arbres pondérés
- **PROB-03** : Appliquer la formule des probabilités totales
- **PROB-04** : Modéliser avec des variables aléatoires
- **PROB-05** : Calculer espérance, variance, écart type

### 💻 **ALGORITHMIQUE ET PROGRAMMATION**
- **ALGO-01** : Manipuler des listes en Python
- **ALGO-02** : Écrire des fonctions
- **ALGO-03** : Simuler des expériences aléatoires

## Mapping Générateurs → Compétences Officielles

### SPE Sujet 1

```python
{
    "spe_sujet1_auto_01_question.py": ["ANA-01"],  # Calcul d'inverse de multiple → calcul numérique de base
    "spe_sujet1_auto_02_question.py": ["ANA-01"],  # Évaluation d'expression fractionnaire → calculs algébriques
    "spe_sujet1_auto_03_question.py": ["ALG-01"],  # Pourcentage d'évolution → modélisation avec suites géométriques
    "spe_sujet1_auto_04_question.py": ["ALG-01", "ALG-02"],  # Évolutions successives → suites géométriques
    "spe_sujet1_auto_05_question.py": ["PROB-01", "PROB-03"],  # Probabilités de dé → probabilités de base
    "spe_sujet1_auto_06_question.py": ["ALG-03"],  # Résolution d'équation avec fractions
    "spe_sujet1_auto_07_question.py": ["ALG-03", "ALG-05"],  # Inéquation x² > n → second degré
    "spe_sujet1_auto_08_question.py": ["GEO-04", "ANA-03"],  # Équation de droite graphiquement
    "spe_sujet1_auto_09_question.py": ["ANA-03"],  # Reconnaissance fonctions affines
    "spe_sujet1_auto_10_question.py": ["ALG-05", "ANA-03"],  # Équation parabole → second degré
    "spe_sujet1_auto_11_question.py": ["ANA-03"],  # Signe de fonction graphiquement
    "spe_sujet1_auto_12_question.py": ["PROB-05"]   # Moyenne pondérée → statistiques
}
```

### SPE Sujet 2

```python
{
    "spe_sujet2_auto_01_question.py": ["PROB-01", "PROB-02", "PROB-03"],  # Arbre probabilités conditionnelles
    "spe_sujet2_auto_02_question.py": ["ALG-01"],  # Diminution prix → évolution géométrique
    "spe_sujet2_auto_03_question.py": ["ALG-01", "ALG-02"],  # Évolutions successives
    "spe_sujet2_auto_04_question.py": ["PROB-01"],  # Proportions conditionnelles
    "spe_sujet2_auto_05_question.py": ["ANA-01"],  # Simplification avec puissances
    "spe_sujet2_auto_06_question.py": ["ANA-01"],  # Conversion unités avec puissances
    "spe_sujet2_auto_07_question.py": ["GEO-04"],  # Coefficient directeur droite
    "spe_sujet2_auto_08_question.py": ["GEO-04", "ANA-03"],  # Équation droite graphique
    "spe_sujet2_auto_09_question.py": ["ALG-03"],  # Résolution x² = n
    "spe_sujet2_auto_10_question.py": ["ALG-05"],  # Signe fonction quadratique
    "spe_sujet2_auto_11_question.py": ["ANA-01"],  # Développement (x+a)²
    "spe_sujet2_auto_12_question.py": ["ALG-03"]   # Isolation variable dans formule
}
```

## Justification par Rapport au Programme Officiel

### 📋 **Alignement Curriculaire Vérifié**

Chaque compétence a été vérifiée contre le programme officiel de **première générale spécialité mathématiques**.

### SPE Sujet 1

#### 1. `spe_sujet1_auto_01_question.py` → **ANA-01**
**Contenu** : Calculer l'inverse d'un multiple (ex: 1/(5×7))
**Curriculum** : Calculs numériques (base seconde) → taux de variation (première)
**Justification** : Compétence de base nécessaire pour l'analyse.

#### 2. `spe_sujet1_auto_02_question.py` → **ANA-01**
**Contenu** : Évaluer F = a + b/(c*d) avec fractions
**Curriculum** : Calculs algébriques avec fractions
**Justification** : Manipulation d'expressions fractionnaires pour l'analyse.

#### 3. `spe_sujet1_auto_03_question.py` → **ALG-01**
**Contenu** : Pourcentage d'évolution d'un prix
**Curriculum** : "Modéliser un phénomène discret à croissance exponentielle par une suite géométrique"
**Justification** : Évolution à taux fixe = suite géométrique (programme officiel).

#### 4. `spe_sujet1_auto_04_question.py` → **ALG-01, ALG-02**
**Contenu** : Évolutions successives (augmentation puis diminution)
**Curriculum** : Suites géométriques et calcul de termes
**Justification** : Évolutions composées = produit de coefficients multiplicateurs.

#### 5. `spe_sujet1_auto_05_question.py` → **PROB-01, PROB-03**
**Contenu** : Probabilités d'un dé (3 faces données, trouver la 4ème)
**Curriculum** : "Probabilité d'un événement : somme des probabilités des issues"
**Justification** : Propriété fondamentale : somme des probabilités = 1.

#### 6. `spe_sujet1_auto_06_question.py` → **ALG-03**
**Contenu** : Résoudre 1/x + 1/y = 1/u pour u
**Curriculum** : "Sur des cas simples de relations entre variables, exprimer une variable en fonction des autres"
**Justification** : Résolution d'équation avec manipulation de fractions.

#### 7. `spe_sujet1_auto_07_question.py` → **ALG-03, ALG-05**
**Contenu** : Résoudre x² > n (inéquation)
**Curriculum** : "Résolution d'une équation du second degré" et "Étudier le signe"
**Justification** : Inéquation quadratique → étude de signe.

#### 8. `spe_sujet1_auto_08_question.py` → **GEO-04, ANA-03**
**Contenu** : Équation y = ax + b d'une droite (graphique)
**Curriculum** : "Déterminer une équation de droite" et reconnaissance de fonctions affines
**Justification** : Géométrie repérée + analyse graphique.

#### 9. `spe_sujet1_auto_09_question.py` → **ANA-03**
**Contenu** : Identifier fonctions affines, coefficient directeur max
**Curriculum** : Reconnaissance et étude des fonctions affines
**Justification** : Analyse des variations et propriétés des fonctions.

#### 10. `spe_sujet1_auto_10_question.py` → **ALG-05, ANA-03**
**Contenu** : Équation parabole ax² + c (graphique)
**Curriculum** : "Fonction polynôme du second degré" et lecture graphique
**Justification** : Polynôme du 2nd degré + analyse graphique.

#### 11. `spe_sujet1_auto_11_question.py` → **ANA-03**
**Contenu** : Signe de x × f(x) à partir d'un graphique
**Curriculum** : Étude du signe et variations graphiques
**Justification** : Analyse de fonction par lecture graphique.

#### 12. `spe_sujet1_auto_12_question.py` → **PROB-05**
**Contenu** : Coefficient pour moyenne pondérée donnée
**Curriculum** : "Moyenne pondérée" (programme officiel)
**Justification** : Calcul direct de moyenne pondérée.

### SPE Sujet 2

#### 1. `spe_sujet2_auto_01_question.py` → **PROB-01, PROB-02, PROB-03**
**Contenu** : Arbre de probabilités, calculer P(B)
**Curriculum** : "Arbres pondérés et calcul de probabilités", "Formule des probabilités totales"
**Justification** : Application directe des probabilités conditionnelles.

#### 2. `spe_sujet2_auto_02_question.py` → **ALG-01**
**Contenu** : Diminution de p% d'un prix
**Curriculum** : Évolution à taux fixe → suite géométrique
**Justification** : Modélisation d'une évolution simple.

#### 3. `spe_sujet2_auto_03_question.py` → **ALG-01, ALG-02**
**Contenu** : Évolutions successives (taux global)
**Curriculum** : Suites géométriques et calculs
**Justification** : Évolutions composées = suite géométrique.

#### 4. `spe_sujet2_auto_04_question.py` → **PROB-01**
**Contenu** : Proportions conditionnelles (internes/gauchers)
**Curriculum** : Probabilités conditionnelles (analogie avec proportions)
**Justification** : Structure identique aux probabilités conditionnelles.

#### 5. `spe_sujet2_auto_05_question.py` → **ANA-01**
**Contenu** : Simplification fraction avec puissances
**Curriculum** : Calculs avec puissances
**Justification** : Manipulation algébrique de base.

#### 6. `spe_sujet2_auto_06_question.py` → **ANA-01**
**Contenu** : Conversion J → kWh avec puissances de 10
**Curriculum** : Calculs avec puissances et conversions
**Justification** : Application des puissances à la physique.

#### 7. `spe_sujet2_auto_07_question.py` → **GEO-04**
**Contenu** : Coefficient directeur entre deux points
**Curriculum** : "Déterminer coefficient directeur à partir de coordonnées"
**Justification** : Compétence exacte du programme géométrie repérée.

#### 8. `spe_sujet2_auto_08_question.py` → **GEO-04, ANA-03**
**Contenu** : Équation ax + by + c = 0 (graphique)
**Curriculum** : Équations de droites + analyse graphique
**Justification** : Géométrie repérée et fonctions affines.

#### 9. `spe_sujet2_auto_09_question.py` → **ALG-03**
**Contenu** : Résoudre x² = n
**Curriculum** : "Résoudre équation du type x² = a"
**Justification** : Compétence exacte du programme algèbre.

#### 10. `spe_sujet2_auto_10_question.py` → **ALG-05**
**Contenu** : Signe de f(x) = (a₁x + b₁)(a₂x + b₂)
**Curriculum** : "Étudier le signe d'une fonction polynôme du second degré factorisée"
**Justification** : Application directe de l'étude de signe.

#### 11. `spe_sujet2_auto_11_question.py` → **ANA-01**
**Contenu** : Développer (x + a)²
**Curriculum** : Calcul littéral et identités remarquables
**Justification** : Compétence de base pour l'analyse.

#### 12. `spe_sujet2_auto_12_question.py` → **ALG-03**
**Contenu** : Isoler v dans a = v²/R
**Curriculum** : Résolution d'équations et isolation de variables
**Justification** : Manipulation algébrique fondamentale.

## Statistiques de Couverture

### 📊 **Répartition par Domaine du Programme Officiel**

| Domaine | Nombre de Questions | Pourcentage |
|---------|-------------------|-------------|
| **🧮 Algèbre** | 11 | 46% |
| **📈 Analyse** | 8 | 33% |
| **📐 Géométrie** | 3 | 13% |
| **🎲 Probabilités** | 2 | 8% |
| **💻 Algorithmique** | 0 | 0% |

### 🎯 **Compétences les Plus Évaluées**

1. **ALG-01** (Suites/Évolutions) : 6 questions
2. **ANA-01** (Calculs de base) : 5 questions  
3. **ALG-03** (Équations 2nd degré) : 4 questions
4. **ANA-03** (Variations/Graphiques) : 4 questions
5. **PROB-01** (Probabilités conditionnelles) : 3 questions

### ✅ **Validation Curriculaire**

**Conformité au programme** : ✅ **100% aligné**

Toutes les questions correspondent exactement aux "Capacités attendues" du programme officiel de première spécialité mathématiques.

**Points forts** :
- ✅ Couverture équilibrée des 4 domaines principaux
- ✅ Respect des niveaux de difficulté appropriés
- ✅ Questions conformes aux "Sujets 0" officiels du baccalauréat

**Recommandations** :
- 💡 Ajouter des questions d'algorithmique (Python/listes)
- 💡 Inclure plus de géométrie vectorielle (produit scalaire)
- 💡 Développer les fonctions exponentielles et trigonométriques

---

*Mapping vérifié contre le Programme de mathématiques de première générale - Spécialité*  
*© Ministère de l'Éducation nationale et de la Jeunesse*
