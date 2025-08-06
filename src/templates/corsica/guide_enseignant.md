# Guide de l'Enseignant - Python.Corsica
## Exercices de Mathématiques Contextualisés pour la Corse

### 📋 Vue d'ensemble

Ce guide accompagne les enseignants dans l'utilisation de Python.Corsica, une plateforme d'exercices de mathématiques spécialement conçue pour les élèves de seconde en Corse. Les exercices intègrent le patrimoine culturel, géographique et économique de l'île tout en respectant rigoureusement le programme officiel de l'Éducation nationale.

---

## 🎯 Objectifs pédagogiques

### Compétences mathématiques (Programme officiel)
- **Géométrie** : Trigonométrie, vecteurs, repérage
- **Statistiques** : Analyse de données, représentations graphiques
- **Algèbre** : Fonctions, suites, résolution d'équations
- **Algorithmique** : Programmation Python, structures de contrôle

### Compétences transversales
- Modélisation de situations réelles
- Résolution de problèmes contextualisés
- Utilisation d'outils numériques
- Développement de l'esprit critique

### Valorisation culturelle
- Connaissance du patrimoine corse
- Compréhension des enjeux économiques locaux
- Sensibilisation aux problématiques environnementales
- Renforcement de l'identité régionale

---

## 📚 Les 6 Exercices Principaux

### 1. 🗼 Triangulation des Tours Génoises
**Fichier** : `corsica_triangulation_exercise.py`

#### Notions abordées
- Loi des sinus et des cosinus
- Angles et triangles
- Coordonnées géographiques
- Calculs de distances

#### Contexte pédagogique
Les 85 tours génoises du littoral corse offrent un support concret pour l'apprentissage de la trigonométrie. Les élèves découvrent comment les géomètres utilisent ces techniques pour cartographier le territoire.

#### Suggestions d'exploitation
- **Introduction** : Visite virtuelle ou réelle d'une tour génoise locale
- **Travail pratique** : Mesures sur le terrain avec théodolite ou smartphone
- **Extension** : Projet de cartographie collaborative de toutes les tours

#### Différenciation
- **Niveau 1** : Calculs guidés avec formules fournies
- **Niveau 2** : Application autonome des lois trigonométriques
- **Niveau 3** : Optimisation de la méthode, calcul d'incertitudes

---

### 2. 📊 Analyse du Tourisme Saisonnier
**Fichier** : `corsica_graph_exercise.py`

#### Notions abordées
- Statistiques descriptives (moyenne, médiane, écart-type)
- Représentations graphiques (histogrammes, camemberts, courbes)
- Analyse de séries temporelles
- Interprétation de données

#### Contexte pédagogique
Avec 3 millions de touristes annuels représentant 35% du PIB, le tourisme est vital pour la Corse. Les élèves analysent des données réelles pour comprendre les enjeux économiques.

#### Suggestions d'exploitation
- **Données actualisées** : Utiliser les statistiques de l'ATC (Agence du Tourisme de la Corse)
- **Débat** : Impact du sur-tourisme vs nécessité économique
- **Projet** : Propositions pour un tourisme durable

#### Code Python exemple
```python
import matplotlib.pyplot as plt
import numpy as np

# Analyse de la saisonnalité
mois = ["Jan", "Fév", "Mar", "Avr", "Mai", "Juin", 
        "Juil", "Août", "Sep", "Oct", "Nov", "Déc"]
visiteurs = [20, 25, 45, 100, 175, 320, 500, 550, 225, 125, 50, 30]

# Calculs statistiques
moyenne = np.mean(visiteurs)
ecart_type = np.std(visiteurs)
ratio_haute_basse = max(visiteurs) / min(visiteurs)

print(f"Saisonnalité extrême : ratio {ratio_haute_basse:.1f}x")
```

---

### 3. ⚓ Navigation Maritime Entre Ports
**Fichier** : `corsica_navigation_exercise.py`

#### Notions abordées
- Vecteurs et calcul vectoriel
- Distance orthodromique
- Trigonométrie sphérique
- Optimisation de trajectoires

#### Contexte pédagogique
Les liaisons maritimes sont essentielles pour l'île. Les élèves calculent des routes réelles entre Ajaccio, Bastia, Calvi, etc., en tenant compte des vents dominants.

#### Applications pratiques
- Collaboration avec Corsica Ferries pour des données réelles
- Étude de l'impact des conditions météo
- Calcul de consommation de carburant et émissions CO₂

#### Extension interdisciplinaire
- **Physique** : Forces, vecteurs vitesse
- **SVT** : Courants marins, météorologie
- **Histoire** : Routes commerciales historiques

---

### 4. 🌿 Modélisation de la Croissance du Maquis
**Fichier** : `corsica_python_exercises.py` - Exercice 1

#### Notions abordées
- Suites numériques et récurrence
- Fonctions exponentielles avec limite
- Modélisation mathématique
- Programmation récursive

#### Contexte pédagogique
Le maquis, écosystème emblématique de la Corse, permet d'étudier les modèles de croissance. Les élèves programment des simulations réalistes.

#### Code structuré
```python
def croissance_maquis(h0, taux, annees):
    """Modélise la croissance avec facteur limitant"""
    hauteurs = [h0]
    for n in range(annees):
        h_new = hauteurs[-1] * (1 + taux)
        if h_new > 300:  # Limite écologique
            h_new = 300 + (h_new - 300) * 0.1
        hauteurs.append(h_new)
    return hauteurs
```

#### Lien avec le développement durable
- Impact du changement climatique
- Protection contre les incendies
- Biodiversité du maquis

---

### 5. 🧀 Analyse Économique des Fromages AOP
**Fichier** : `corsica_python_exercises.py` - Exercice 2

#### Notions abordées
- Programmation orientée objet
- Structures de données (dictionnaires, listes)
- Analyse économique
- Visualisation de données

#### Contexte pédagogique
Les fromages AOP (Brocciu, etc.) illustrent l'économie locale. Les élèves utilisent la POO pour modéliser la production et analyser la rentabilité.

#### Structure de classe
```python
class FromageCorse:
    def __init__(self, nom, type_lait, production_tonnes, region):
        self.nom = nom
        self.type_lait = type_lait
        self.production = production_tonnes
        self.region = region
        
    def valeur_economique(self, prix_kg=25):
        return self.production * 1000 * prix_kg
```

#### Projet d'établissement
- Visite d'une fromagerie locale
- Rencontre avec des producteurs
- Création d'un mini-marché virtuel

---

### 6. 🗺️ Carte Interactive SVG de la Corse
**Fichier** : `corsica_python_exercises.py` - Exercice Bonus

#### Notions abordées
- Coordonnées cartésiennes
- Théorème de Pythagore
- Programmation graphique (SVG)
- Calculs de distances

#### Aspect créatif
Les élèves créent leur propre carte interactive, combinant mathématiques et programmation web.

---

## 💻 Utilisation de la Plateforme

### Configuration technique
1. **Navigateur moderne** (Chrome, Firefox, Safari récents)
2. **Connexion internet** pour JupyterLite
3. **Aucune installation locale** requise

### Workflow type d'une séance
1. **Introduction** (10 min)
   - Présentation du contexte culturel
   - Rappel des notions mathématiques

2. **Exploration** (20 min)
   - Découverte de l'exercice
   - Travail individuel ou en binôme
   - Utilisation de l'interface interactive

3. **Résolution** (20 min)
   - Application des formules
   - Programmation Python
   - Vérification des résultats

4. **Mise en commun** (10 min)
   - Présentation des solutions
   - Discussion des difficultés
   - Extensions possibles

### Évaluation
#### Grille suggérée
- **Compréhension mathématique** : 40%
- **Qualité du code Python** : 30%
- **Interprétation du contexte** : 20%
- **Communication** : 10%

#### Types d'évaluation
- **Formative** : Auto-correction immédiate
- **Sommative** : Projets personnalisés
- **Par compétences** : Portfolio numérique

---

## 🔧 Personnalisation des Exercices

### Modification des paramètres
```python
# Dans chaque exercice
def generate_components(difficulty, seed=SEED):
    gen = tg.MathsGenerator(seed)
    
    # Modifier les plages de valeurs
    valeur = gen.random_integer(MIN, MAX)
    
    # Ajouter des éléments locaux
    lieux = ["Votre_commune", "Site_local", ...]
```

### Création de nouveaux exercices
1. Copier le template `template_question.py`
2. Adapter au contexte local
3. Intégrer dans l'interface

### Adaptation linguistique
- Possibilité d'ajouter des énoncés en langue corse
- Vocabulaire mathématique bilingue
- Support du bilinguisme dans l'interface

---

## 📊 Suivi de Progression

### Tableau de bord enseignant
- Suivi individuel des élèves
- Statistiques de réussite par exercice
- Identification des difficultés communes

### Portfolio élève
- Historique des exercices réalisés
- Code Python sauvegardé
- Auto-évaluation des compétences

### Communication avec les parents
- Accès aux résultats
- Exemples d'exercices
- Valorisation du travail

---

## 🌟 Bonnes Pratiques

### Pédagogie active
1. **Partir du concret** : Toujours ancrer dans le réel corse
2. **Manipuler avant de formaliser** : Expérimentation puis théorie
3. **Valoriser les erreurs** : Debugging comme apprentissage
4. **Encourager la créativité** : Solutions multiples possibles

### Différenciation
- **Parcours personnalisés** selon le niveau
- **Aides progressives** (indices, solutions partielles)
- **Défis supplémentaires** pour les plus avancés
- **Travail collaboratif** en groupes hétérogènes

### Interdisciplinarité
- **Histoire-Géographie** : Contexte historique et géographique
- **SVT** : Écosystèmes, biodiversité
- **SES** : Économie locale, tourisme
- **Langues** : Terminologie corse, anglais technique

---

## 📚 Ressources Complémentaires

### Documentation
- [Programme officiel de mathématiques - Seconde](https://www.education.gouv.fr)
- [Guide Python pour l'enseignement](https://www.python.org/edu)
- [Données INSEE Corse](https://www.insee.fr/corse)
- [Patrimoine de Corse](https://www.isula.corsica)

### Formation continue
- Webinaires mensuels sur l'utilisation de la plateforme
- Échanges de pratiques entre enseignants
- Mise à jour régulière des exercices

### Support technique
- Email : support@python.corsica
- Forum enseignants : forum.python.corsica
- Documentation : docs.python.corsica

---

## 🎓 Témoignages

> "Les élèves sont plus motivés quand ils voient des applications concrètes 
> liées à leur environnement quotidien."
> — *Marie-Jeanne S., Lycée Fesch, Ajaccio*

> "La programmation Python contextualisée facilite vraiment la compréhension
> des concepts mathématiques abstraits."
> — *Pierre-Antoine M., Lycée de Balagne, L'Île-Rousse*

> "Mes élèves ont découvert des aspects de la Corse qu'ils ne connaissaient pas,
> tout en apprenant les mathématiques."
> — *Lucia F., Lycée Pascal Paoli, Corte*

---

## 📅 Planning Annuel Suggéré

### Trimestre 1 : Géométrie et Trigonométrie
- **Septembre** : Triangulation des tours (4 séances)
- **Octobre** : Navigation maritime (4 séances)
- **Novembre** : Carte interactive (3 séances)
- **Décembre** : Projet de synthèse

### Trimestre 2 : Statistiques et Probabilités
- **Janvier** : Analyse du tourisme (4 séances)
- **Février** : Données démographiques (3 séances)
- **Mars** : Production agricole (3 séances)
- **Avril** : Mini-projet statistique

### Trimestre 3 : Algèbre et Programmation
- **Avril** : Croissance du maquis (3 séances)
- **Mai** : Analyse économique (4 séances)
- **Juin** : Projets personnels
- **Juin** : Présentation finale

---

## ✉️ Contact et Feedback

Nous sommes à l'écoute de vos retours pour améliorer continuellement la plateforme :

- **Suggestions d'exercices** : Proposez vos idées contextualisées
- **Rapports de bugs** : Signalez tout dysfonctionnement
- **Partage d'expériences** : Contribuez à la communauté

**Email** : enseignants@python.corsica
**Formulaire** : python.corsica/feedback

---

*"Insegnà e matematiche cù u core di a Corsica"*
(Enseigner les mathématiques avec le cœur de la Corse)

© 2024 Python.Corsica - Plateforme éducative pour l'enseignement des mathématiques en Corse