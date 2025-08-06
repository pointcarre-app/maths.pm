# Recommandations d'exercices de mathématiques pour la Corse
## Niveau Seconde - Programme officiel adapté au contexte insulaire

### 🎯 Objectifs pédagogiques
- Ancrer l'apprentissage des mathématiques dans le contexte culturel et géographique corse
- Respecter le programme officiel de l'Éducation nationale pour la classe de seconde
- Développer les compétences en programmation Python
- Valoriser le patrimoine et l'identité corse à travers les mathématiques

---

## 📐 1. GÉOMÉTRIE ET TRIGONOMÉTRIE

### Exercice 1.1 : Triangulation des tours génoises
**[Déjà implémenté - voir corsica_triangulation_exercise.py]**
- **Compétences** : Trigonométrie, loi des sinus, résolution de triangles
- **Contexte** : Localisation des 85 tours génoises du littoral corse
- **Niveau** : ⭐⭐⭐

### Exercice 1.2 : Navigation maritime traditionnelle
- **Thème** : Calcul de routes maritimes entre les ports corses (Ajaccio, Bastia, Calvi, Porto-Vecchio)
- **Concepts** : Coordonnées GPS, angles de navigation, distance orthodromique
- **Application** : Optimisation des trajets des ferries Corsica Ferries et La Méridionale
- **Niveau** : ⭐⭐⭐

### Exercice 1.3 : Architecture des citadelles
- **Thème** : Étude géométrique des fortifications (Citadelle de Calvi, Bonifacio)
- **Concepts** : Polygones réguliers, angles, symétries
- **Bonus culturel** : Histoire de la défense de l'île contre les invasions
- **Niveau** : ⭐⭐

---

## 📊 2. STATISTIQUES ET PROBABILITÉS

### Exercice 2.1 : Analyse du tourisme saisonnier
**[Déjà implémenté - voir corsica_graph_exercise.py]**
- **Compétences** : Statistiques descriptives, représentations graphiques
- **Contexte** : 3 millions de touristes annuels, impact économique (35% du PIB)
- **Niveau** : ⭐⭐

### Exercice 2.2 : Étude démographique
- **Thème** : Évolution de la population corse (1960-2024)
- **Données** : Migration, pyramide des âges, répartition urbain/rural
- **Concepts** : Taux de variation, interpolation, projection
- **Application** : Problématique du vieillissement et de l'exode rural
- **Niveau** : ⭐⭐

### Exercice 2.3 : Production agricole AOP
- **Thème** : Analyse de la production (clémentines de Corse, vin de Patrimonio, huile d'olive)
- **Concepts** : Moyennes pondérées, écart-type, corrélation climat/rendement
- **Bonus** : Impact du changement climatique sur l'agriculture insulaire
- **Niveau** : ⭐⭐⭐

---

## 🖥️ 3. PROGRAMMATION PYTHON

### Exercice 3.1 : Modélisation écologique du maquis
**[Déjà implémenté - voir corsica_python_exercises.py]**
- **Compétences** : Suites, fonctions, matplotlib
- **Contexte** : Croissance de la végétation endémique (ciste, myrte, arbousier)
- **Niveau** : ⭐⭐

### Exercice 3.2 : Analyse économique des fromages AOP
**[Déjà implémenté - voir corsica_python_exercises.py]**
- **Compétences** : POO, structures de données, visualisation
- **Contexte** : Brocciu et autres fromages traditionnels
- **Niveau** : ⭐⭐⭐

### Exercice 3.3 : Simulation météorologique
- **Thème** : Prévision des vents (Libeccio, Tramontane, Gregale)
- **Concepts** : Vecteurs, modélisation, numpy
- **Application** : Impact sur la navigation et les incendies
- **Code suggéré** :
```python
import numpy as np
import matplotlib.pyplot as plt

def simuler_vents_corses(jour_annee):
    """Simule les vents dominants selon la saison"""
    vents = {
        'Libeccio': {'direction': 225, 'force_ete': 40, 'force_hiver': 60},
        'Tramontane': {'direction': 315, 'force_ete': 30, 'force_hiver': 50},
        'Gregale': {'direction': 45, 'force_ete': 25, 'force_hiver': 45}
    }
    # Simulation saisonnière...
```
- **Niveau** : ⭐⭐⭐

---

## 📈 4. FONCTIONS ET ALGÈBRE

### Exercice 4.1 : Modélisation des marées
- **Thème** : Variation du niveau de la mer dans les ports corses
- **Concepts** : Fonctions sinusoïdales, périodicité, amplitude
- **Formule** : h(t) = A·sin(ωt + φ) + h₀
- **Application** : Planification des activités portuaires
- **Niveau** : ⭐⭐⭐

### Exercice 4.2 : Croissance de la population de mouflons
- **Thème** : Évolution de l'espèce endémique dans le Parc naturel régional
- **Concepts** : Fonction exponentielle limitée, capacité d'accueil
- **Modèle** : P(t) = K / (1 + A·e^(-rt))
- **Niveau** : ⭐⭐⭐⭐

### Exercice 4.3 : Rentabilité de la châtaigneraie
- **Thème** : Analyse économique de la production de farine de châtaigne
- **Concepts** : Fonctions coût/recette, optimisation, dérivées
- **Contexte** : La Castagniccia, région historique de production
- **Niveau** : ⭐⭐⭐

---

## 🏔️ 5. GÉOMÉTRIE DANS L'ESPACE

### Exercice 5.1 : Topographie du Monte Cinto
- **Thème** : Modélisation 3D du plus haut sommet corse (2706 m)
- **Concepts** : Coordonnées 3D, plans, courbes de niveau
- **Application** : Calcul de pentes pour les sentiers de randonnée (GR20)
- **Niveau** : ⭐⭐⭐⭐

### Exercice 5.2 : Volume des réservoirs d'eau
- **Thème** : Gestion de l'eau dans les barrages (Tolla, Calacuccia)
- **Concepts** : Calcul de volumes, intégration numérique
- **Enjeu** : Autonomie hydrique de l'île
- **Niveau** : ⭐⭐⭐

---

## 🎨 6. EXERCICES CRÉATIFS ET INTERDISCIPLINAIRES

### Exercice 6.1 : Fractales dans l'art corse
- **Thème** : Motifs géométriques dans l'artisanat (dentelle, vannerie)
- **Concepts** : Récursivité, symétries, transformations
- **Code Python** : Génération de motifs avec turtle ou SVG
- **Niveau** : ⭐⭐

### Exercice 6.2 : Optimisation des circuits touristiques
- **Thème** : Problème du voyageur de commerce appliqué aux sites touristiques
- **Sites** : Scandola, Bavella, Restonica, Calanques de Piana
- **Concepts** : Graphes, algorithmes, distances
- **Niveau** : ⭐⭐⭐⭐

### Exercice 6.3 : Acoustique des polyphonies
- **Thème** : Analyse mathématique des chants traditionnels (paghjella)
- **Concepts** : Fréquences, harmoniques, transformée de Fourier
- **Application** : Visualisation des spectres sonores avec matplotlib
- **Niveau** : ⭐⭐⭐⭐

---

## 💡 RECOMMANDATIONS PÉDAGOGIQUES

### Pour les enseignants

1. **Contextualisation systématique**
   - Utiliser des exemples locaux pour chaque notion
   - Inviter des professionnels corses (géomètres, agriculteurs, météorologues)
   - Organiser des sorties pédagogiques (tours génoises, observatoire météo)

2. **Approche bilingue**
   - Introduire le vocabulaire mathématique en corse
   - Exemples : triangulu (triangle), angulu (angle), numeru (nombre)
   - Valoriser le bilinguisme dans la résolution de problèmes

3. **Projets collaboratifs**
   - Partenariat avec l'Université de Corse (Università di Corsica)
   - Participation aux Olympiades de mathématiques avec thématique insulaire
   - Création d'une base de données d'exercices contextualisés

### Pour les élèves

1. **Développement de l'autonomie**
   - Utilisation de JupyterLite pour expérimenter
   - Création de portfolios numériques de projets
   - Auto-évaluation avec les QCM générés

2. **Liens avec l'orientation**
   - Métiers locaux utilisant les mathématiques
   - Témoignages d'anciens élèves
   - Stages dans les entreprises corses (DPLC, EDF Corse, etc.)

---

## 📚 RESSOURCES COMPLÉMENTAIRES

### Sites web recommandés
- **INSEE Corse** : Données statistiques actualisées
- **Météo France Corse** : Données climatiques pour modélisation
- **IGN** : Cartes topographiques pour exercices de géométrie
- **Collectivité de Corse** : Données économiques et touristiques

### Bibliographie
- "Mathématiques et patrimoine corse" - Guide pédagogique
- "Le GR20 en équations" - Applications de la trigonométrie
- "Statistiques insulaires" - Analyse de données régionales

### Outils numériques
- **GeoGebra** : Constructions géométriques dynamiques
- **Python/Matplotlib** : Visualisation de données
- **QGIS** : Cartographie et géolocalisation
- **Scratch** : Introduction à l'algorithmique

---

## 🎯 ÉVALUATION ET PROGRESSION

### Critères d'évaluation adaptés
1. **Compréhension mathématique** (40%)
2. **Application au contexte corse** (30%)
3. **Qualité de la programmation** (20%)
4. **Communication et présentation** (10%)

### Progression suggérée
- **Trimestre 1** : Géométrie et trigonométrie (tours, navigation)
- **Trimestre 2** : Statistiques et probabilités (tourisme, démographie)
- **Trimestre 3** : Fonctions et programmation (modélisation, optimisation)

### Différenciation pédagogique
- **Niveau débutant** : Exercices guidés avec code pré-rempli
- **Niveau intermédiaire** : Problèmes ouverts avec aide méthodologique
- **Niveau avancé** : Projets de recherche et création d'exercices

---

## 🌟 CONCLUSION

Ces exercices visent à :
- **Renforcer l'identité culturelle** tout en maîtrisant les mathématiques
- **Préparer aux études supérieures** avec des bases solides
- **Développer l'esprit critique** face aux enjeux locaux
- **Favoriser l'innovation** dans l'approche pédagogique

L'objectif est de faire des mathématiques un outil de compréhension et de valorisation du territoire corse, tout en respectant les exigences du programme national.

---

*"A matematica hè a lingua di a natura, è a Corsica hè u nostru laboratoriu"*
(Les mathématiques sont le langage de la nature, et la Corse est notre laboratoire)