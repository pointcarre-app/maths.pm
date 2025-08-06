"""
Exercices Python pour le niveau seconde : Programmation et modélisation
Thématique : La Corse et ses particularités
"""

import teachers.generator as tg
from teachers.defaults import SEED


def generate_python_exercise_1(difficulty, seed=SEED) -> dict:
    """
    Exercice Python 1 : Modélisation de la croissance du maquis corse
    Utilisation de suites et de matplotlib
    """
    gen = tg.MathsGenerator(seed)

    # Paramètres de croissance du maquis
    hauteur_initiale = gen.random_integer(10, 30)  # cm
    taux_croissance = gen.random_integer(15, 25) / 100  # pourcentage
    duree_annees = gen.random_integer(5, 10)

    code_template = f"""
# Exercice 1 : Modélisation de la croissance du maquis corse
# Le maquis est la végétation emblématique de la Corse

import matplotlib.pyplot as plt
import numpy as np

def croissance_maquis(hauteur_initiale, taux_croissance, annees):
    \"\"\"
    Modélise la croissance du maquis corse.
    
    Le maquis corse est composé de :
    - Ciste, Myrte, Arbousier (croissance rapide)
    - Bruyère, Lentisque (croissance moyenne)
    - Chêne vert (croissance lente)
    \"\"\"
    hauteurs = [hauteur_initiale]
    
    for annee in range(1, annees + 1):
        # Formule de croissance exponentielle avec facteur limitant
        nouvelle_hauteur = hauteurs[-1] * (1 + taux_croissance)
        
        # Facteur limitant (le maquis ne dépasse pas 3-4 mètres)
        if nouvelle_hauteur > 300:  # 300 cm = 3 mètres
            nouvelle_hauteur = 300 + (nouvelle_hauteur - 300) * 0.1
        
        hauteurs.append(nouvelle_hauteur)
    
    return hauteurs

# Paramètres de l'exercice
hauteur_initiale = {hauteur_initiale}  # cm
taux_croissance = {taux_croissance}  # taux annuel
duree = {duree_annees}  # années

# Calcul de la croissance
hauteurs = croissance_maquis(hauteur_initiale, taux_croissance, duree)

# Visualisation
plt.figure(figsize=(12, 6))

# Graphique 1 : Évolution temporelle
plt.subplot(1, 2, 1)
annees = list(range(duree + 1))
plt.plot(annees, hauteurs, 'g-', linewidth=2, marker='o', markersize=6)
plt.fill_between(annees, 0, hauteurs, alpha=0.3, color='green')
plt.xlabel('Années', fontsize=12)
plt.ylabel('Hauteur (cm)', fontsize=12)
plt.title('Croissance du maquis corse', fontsize=14, fontweight='bold')
plt.grid(True, alpha=0.3)

# Ajouter des annotations pour les espèces typiques
plt.axhline(y=50, color='brown', linestyle='--', alpha=0.5, label='Ciste')
plt.axhline(y=150, color='darkgreen', linestyle='--', alpha=0.5, label='Myrte')
plt.axhline(y=300, color='olive', linestyle='--', alpha=0.5, label='Arbousier')
plt.legend(loc='lower right')

# Graphique 2 : Taux de croissance annuel
plt.subplot(1, 2, 2)
taux_annuels = []
for i in range(1, len(hauteurs)):
    taux = ((hauteurs[i] - hauteurs[i-1]) / hauteurs[i-1]) * 100
    taux_annuels.append(taux)

plt.bar(annees[1:], taux_annuels, color='forestgreen', edgecolor='black', alpha=0.7)
plt.xlabel('Année', fontsize=12)
plt.ylabel('Taux de croissance (%)', fontsize=12)
plt.title('Taux de croissance annuel', fontsize=14, fontweight='bold')
plt.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.show()

# Questions à résoudre :
print("\\n🌿 Analyse de la croissance du maquis corse")
print("=" * 50)
print(f"1. Hauteur initiale : {{hauteur_initiale}} cm")
print(f"2. Hauteur finale après {{duree}} ans : {{hauteurs[-1]:.1f}} cm")
print(f"3. Croissance totale : {{hauteurs[-1] - hauteur_initiale:.1f}} cm")
print(f"4. Croissance moyenne annuelle : {{(hauteurs[-1] - hauteur_initiale) / duree:.1f}} cm/an")

# Calcul du temps pour atteindre une certaine hauteur
hauteur_cible = 200  # cm
for i, h in enumerate(hauteurs):
    if h >= hauteur_cible:
        print(f"5. Temps pour atteindre {{hauteur_cible}} cm : {{i}} ans")
        break

# Bonus : Création d'une fonction récursive
def maquis_recursif(h, taux, n):
    \"\"\"Calcul récursif de la hauteur après n années\"\"\"
    if n == 0:
        return h
    else:
        nouvelle_h = h * (1 + taux)
        if nouvelle_h > 300:
            nouvelle_h = 300 + (nouvelle_h - 300) * 0.1
        return maquis_recursif(nouvelle_h, taux, n - 1)

hauteur_recursive = maquis_recursif(hauteur_initiale, taux_croissance, duree)
print(f"\\n6. Vérification par méthode récursive : {{hauteur_recursive:.1f}} cm")
"""

    return {
        "titre": "Modélisation de la croissance du maquis corse",
        "code": code_template,
        "hauteur_initiale": hauteur_initiale,
        "taux_croissance": taux_croissance,
        "duree": duree_annees,
        "competences": ["Suites numériques", "Fonctions", "Programmation", "Visualisation"],
    }


def generate_python_exercise_2(difficulty, seed=SEED) -> dict:
    """
    Exercice Python 2 : Analyse de la production de fromages corses (AOP)
    Utilisation de dictionnaires, listes et création de graphiques
    """
    gen = tg.MathsGenerator(seed)

    # Données sur les fromages AOP corses
    production_brocciu = gen.random_integer(1500, 2500)  # tonnes
    production_autres = gen.random_integer(800, 1200)  # tonnes

    code_template = f"""
# Exercice 2 : Analyse de la production de fromages corses AOP
# La Corse possède plusieurs fromages avec Appellation d'Origine Protégée

import matplotlib.pyplot as plt
import numpy as np

class FromageCorse:
    \"\"\"Classe représentant un fromage corse\"\"\"
    
    def __init__(self, nom, type_lait, production_tonnes, region):
        self.nom = nom
        self.type_lait = type_lait
        self.production = production_tonnes
        self.region = region
        self.aop = True  # Tous nos fromages ont l'AOP
    
    def __str__(self):
        return f"{{self.nom}} ({{self.type_lait}}) - {{self.production}}t/an - {{self.region}}"
    
    def valeur_economique(self, prix_kg=25):
        \"\"\"Calcule la valeur économique en euros\"\"\"
        return self.production * 1000 * prix_kg

# Création des fromages corses
fromages = [
    FromageCorse("Brocciu", "Brebis/Chèvre", {production_brocciu}, "Toute la Corse"),
    FromageCorse("Calinzana", "Chèvre", {gen.random_integer(50, 100)}, "Balagne"),
    FromageCorse("Venachese", "Brebis", {gen.random_integer(30, 60)}, "Centre Corse"),
    FromageCorse("Niolo", "Brebis", {gen.random_integer(40, 80)}, "Niolo"),
    FromageCorse("Bastelicaccia", "Brebis", {gen.random_integer(60, 90)}, "Ajaccio"),
    FromageCorse("Sartinesu", "Chèvre", {gen.random_integer(35, 65)}, "Sartenais"),
]

# Analyse de la production
def analyser_production(fromages_list):
    \"\"\"Analyse la production de fromages corses\"\"\"
    
    # Production totale
    production_totale = sum(f.production for f in fromages_list)
    
    # Production par type de lait
    production_par_lait = {{}}
    for f in fromages_list:
        if f.type_lait not in production_par_lait:
            production_par_lait[f.type_lait] = 0
        production_par_lait[f.type_lait] += f.production
    
    # Production par région
    production_par_region = {{}}
    for f in fromages_list:
        if f.region not in production_par_region:
            production_par_region[f.region] = 0
        production_par_region[f.region] += f.production
    
    return production_totale, production_par_lait, production_par_region

# Calculs
total, par_lait, par_region = analyser_production(fromages)

# Visualisation
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("Production de fromages AOP en Corse", fontsize=16, fontweight='bold')

# 1. Diagramme en barres - Production par fromage
ax1 = axes[0, 0]
noms = [f.nom for f in fromages]
productions = [f.production for f in fromages]
colors = plt.cm.Set3(np.linspace(0, 1, len(noms)))
bars = ax1.bar(noms, productions, color=colors, edgecolor='black')
ax1.set_xlabel('Fromage', fontsize=12)
ax1.set_ylabel('Production (tonnes/an)', fontsize=12)
ax1.set_title('Production par type de fromage', fontsize=14)
ax1.tick_params(axis='x', rotation=45)

# Ajouter les valeurs sur les barres
for bar, prod in zip(bars, productions):
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height + 10,
             f'{{prod}}t', ha='center', va='bottom', fontsize=9)

# 2. Camembert - Répartition par type de lait
ax2 = axes[0, 1]
lait_labels = list(par_lait.keys())
lait_values = list(par_lait.values())
wedges, texts, autotexts = ax2.pie(lait_values, labels=lait_labels, 
                                     autopct='%1.1f%%', startangle=90,
                                     colors=['#FFB6C1', '#87CEEB', '#98FB98'])
ax2.set_title('Répartition par type de lait', fontsize=14)

# 3. Graphique en aires empilées - Évolution simulée sur 5 ans
ax3 = axes[1, 0]
annees = list(range(2020, 2025))
# Simulation d'une croissance
croissance = [1.0, 1.03, 1.05, 1.08, 1.10]
productions_evolution = []
for f in fromages[:3]:  # Top 3 fromages
    prod_annees = [f.production * c for c in croissance]
    productions_evolution.append(prod_annees)

ax3.stackplot(annees, *productions_evolution, labels=[f.nom for f in fromages[:3]],
              alpha=0.8, colors=['#FF9999', '#66B2FF', '#99FF99'])
ax3.set_xlabel('Année', fontsize=12)
ax3.set_ylabel('Production (tonnes)', fontsize=12)
ax3.set_title('Évolution de la production (projection)', fontsize=14)
ax3.legend(loc='upper left')
ax3.grid(True, alpha=0.3)

# 4. Carte de valeur économique
ax4 = axes[1, 1]
valeurs = [f.valeur_economique() / 1e6 for f in fromages]  # En millions d'euros
y_pos = np.arange(len(noms))
bars = ax4.barh(y_pos, valeurs, color='gold', edgecolor='black')
ax4.set_yticks(y_pos)
ax4.set_yticklabels(noms)
ax4.set_xlabel('Valeur économique (M€)', fontsize=12)
ax4.set_title('Impact économique des fromages AOP', fontsize=14)
ax4.grid(axis='x', alpha=0.3)

# Ajouter les valeurs
for bar, val in zip(bars, valeurs):
    width = bar.get_width()
    ax4.text(width + 0.5, bar.get_y() + bar.get_height()/2,
             f'{{val:.1f}}M€', ha='left', va='center', fontsize=9)

plt.tight_layout()
plt.show()

# Rapport d'analyse
print("\\n🧀 Analyse de la filière fromage AOP en Corse")
print("=" * 60)
print(f"Production totale : {{total}} tonnes/an")
print(f"Valeur économique totale : {{sum(valeurs):.1f}} millions d'euros")
print(f"\\nProduction par type de lait :")
for lait, prod in par_lait.items():
    print(f"  - {{lait}} : {{prod}} tonnes ({{prod/total*100:.1f}}%)")

print(f"\\nFromage le plus produit : {{max(fromages, key=lambda x: x.production).nom}}")
print(f"Fromage à plus forte valeur : {{max(fromages, key=lambda x: x.valeur_economique()).nom}}")

# Exercice supplémentaire : Optimisation
def optimiser_production(budget_euros, cout_tonne=5000):
    \"\"\"
    Détermine combien de tonnes supplémentaires peuvent être produites
    avec un budget donné pour moderniser les exploitations.
    \"\"\"
    tonnes_supplementaires = budget_euros / cout_tonne
    nouvelle_production = total + tonnes_supplementaires
    augmentation_pourcent = (tonnes_supplementaires / total) * 100
    
    return {{
        'tonnes_supplementaires': tonnes_supplementaires,
        'nouvelle_production': nouvelle_production,
        'augmentation_pourcent': augmentation_pourcent
    }}

# Simulation d'investissement
investissement = 2_000_000  # 2 millions d'euros
resultat = optimiser_production(investissement)
print(f"\\nAvec un investissement de {{investissement/1e6:.1f}}M€ :")
print(f"  - Production supplémentaire : {{resultat['tonnes_supplementaires']:.0f}} tonnes")
print(f"  - Augmentation : +{{resultat['augmentation_pourcent']:.1f}}%")
"""

    return {
        "titre": "Analyse de la production de fromages corses AOP",
        "code": code_template,
        "production_brocciu": production_brocciu,
        "competences": ["Classes et objets", "Dictionnaires", "Analyse de données", "Graphiques"],
    }


def generate_svg_exercise(difficulty, seed=SEED) -> dict:
    """
    Exercice bonus : Création d'une carte interactive de la Corse en SVG
    """
    gen = tg.MathsGenerator(seed)

    svg_code = """
# Exercice bonus : Carte interactive de la Corse en SVG

def creer_carte_corse():
    \"\"\"
    Crée une carte simplifiée de la Corse en SVG avec les principales villes
    et des informations mathématiques (distances, populations, etc.)
    \"\"\"
    
    svg = \"\"\"
    <svg viewBox="0 0 300 400" xmlns="http://www.w3.org/2000/svg">
        <!-- Fond de carte -->
        <rect width="300" height="400" fill="#E6F3FF"/>
        
        <!-- Forme simplifiée de la Corse -->
        <path d="M 150 50 
                 Q 180 60, 190 100
                 L 195 150
                 Q 200 200, 185 250
                 L 170 320
                 Q 160 360, 150 380
                 Q 140 360, 130 320
                 L 115 250
                 Q 100 200, 105 150
                 L 110 100
                 Q 120 60, 150 50 Z"
              fill="#90EE90" 
              stroke="#228B22" 
              stroke-width="2"/>
        
        <!-- Cap Corse -->
        <ellipse cx="150" cy="60" rx="15" ry="30" 
                 fill="#90EE90" stroke="#228B22" stroke-width="2"/>
        
        <!-- Villes principales -->
        <!-- Bastia -->
        <circle cx="165" cy="80" r="5" fill="red"/>
        <text x="175" y="82" font-size="12" font-weight="bold">Bastia</text>
        
        <!-- Ajaccio -->
        <circle cx="120" cy="200" r="5" fill="red"/>
        <text x="80" y="202" font-size="12" font-weight="bold">Ajaccio</text>
        
        <!-- Corte -->
        <circle cx="150" cy="160" r="4" fill="blue"/>
        <text x="160" y="162" font-size="11">Corte</text>
        
        <!-- Porto-Vecchio -->
        <circle cx="170" cy="320" r="4" fill="red"/>
        <text x="180" y="322" font-size="11">Porto-Vecchio</text>
        
        <!-- Calvi -->
        <circle cx="115" cy="110" r="4" fill="red"/>
        <text x="70" y="112" font-size="11">Calvi</text>
        
        <!-- Bonifacio -->
        <circle cx="155" cy="370" r="4" fill="red"/>
        <text x="165" y="372" font-size="11">Bonifacio</text>
        
        <!-- Titre -->
        <text x="150" y="30" text-anchor="middle" 
              font-size="18" font-weight="bold" fill="#2C3E50">
            Carte de la Corse
        </text>
        
        <!-- Légende des distances -->
        <text x="10" y="390" font-size="10" fill="#555">
            Distances : Ajaccio-Bastia: 147km | Ajaccio-Bonifacio: 131km
        </text>
        
        <!-- Échelle -->
        <line x1="250" y1="360" x2="280" y2="360" stroke="black" stroke-width="2"/>
        <text x="255" y="375" font-size="9">50 km</text>
        
        <!-- Rose des vents -->
        <g transform="translate(250, 50)">
            <line x1="0" y1="-15" x2="0" y2="15" stroke="black" stroke-width="1"/>
            <line x1="-15" y1="0" x2="15" y2="0" stroke="black" stroke-width="1"/>
            <text x="0" y="-20" text-anchor="middle" font-size="10">N</text>
        </g>
        
        <!-- Informations statistiques -->
        <text x="10" y="20" font-size="9" fill="#666">
            Superficie: 8 680 km²
        </text>
        <text x="10" y="35" font-size="9" fill="#666">
            Population: 349 465 hab.
        </text>
        <text x="10" y="50" font-size="9" fill="#666">
            Point culminant: Monte Cinto (2 706 m)
        </text>
    </svg>
    \"\"\"
    
    return svg

# Fonction pour calculer les distances entre villes (théorème de Pythagore)
def distance_entre_villes(ville1, ville2):
    \"\"\"
    Calcule la distance entre deux villes en utilisant leurs coordonnées.
    Utilise une échelle où 1 pixel = 2 km environ.
    \"\"\"
    villes = {
        "Ajaccio": (120, 200),
        "Bastia": (165, 80),
        "Corte": (150, 160),
        "Porto-Vecchio": (170, 320),
        "Calvi": (115, 110),
        "Bonifacio": (155, 370)
    }
    
    if ville1 in villes and ville2 in villes:
        x1, y1 = villes[ville1]
        x2, y2 = villes[ville2]
        
        # Théorème de Pythagore
        distance_pixels = ((x2 - x1)**2 + (y2 - y1)**2)**0.5
        distance_km = distance_pixels * 2  # Échelle approximative
        
        return round(distance_km, 1)
    return None

# Calcul du périmètre approximatif de l'île
def perimetre_corse():
    \"\"\"
    Calcule le périmètre approximatif de la Corse
    en utilisant les points du contour SVG.
    \"\"\"
    # Points approximatifs du contour (simplifiés)
    points = [
        (150, 50), (190, 100), (195, 150), (185, 250),
        (170, 320), (150, 380), (130, 320), (115, 250),
        (105, 150), (110, 100), (150, 50)
    ]
    
    perimetre = 0
    for i in range(len(points) - 1):
        x1, y1 = points[i]
        x2, y2 = points[i + 1]
        segment = ((x2 - x1)**2 + (y2 - y1)**2)**0.5
        perimetre += segment
    
    # Conversion en km (échelle)
    perimetre_km = perimetre * 2
    return round(perimetre_km, 0)

# Tests
print("🗺️ Carte Interactive de la Corse")
print("=" * 40)
print(f"Distance Ajaccio-Bastia : {distance_entre_villes('Ajaccio', 'Bastia')} km")
print(f"Distance Ajaccio-Corte : {distance_entre_villes('Ajaccio', 'Corte')} km")
print(f"Distance Bastia-Bonifacio : {distance_entre_villes('Bastia', 'Bonifacio')} km")
print(f"Périmètre approximatif : {perimetre_corse()} km")
print("(Périmètre réel : environ 1 000 km)")
"""

    return {
        "titre": "Carte interactive de la Corse en SVG",
        "code": svg_code,
        "competences": ["Géométrie", "Coordonnées", "SVG", "Théorème de Pythagore"],
    }


def generate_all_exercises(difficulty=None, seed=SEED):
    """
    Génère tous les exercices Python pour la Corse.
    """
    exercises = {
        "exercice_1": generate_python_exercise_1(difficulty, seed),
        "exercice_2": generate_python_exercise_2(difficulty, seed),
        "exercice_bonus": generate_svg_exercise(difficulty, seed),
    }

    return exercises
