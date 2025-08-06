"""
Exercice de navigation maritime : Routes entre les ports corses
Pour le niveau seconde - Vecteurs et trigonométrie
"""

import teachers.generator as tg
import teachers.maths as tm
from teachers.defaults import SEED
import math


def generate_components(difficulty, seed=SEED) -> dict:
    """
    Génère un exercice de navigation maritime entre les ports corses.
    L'élève doit calculer cap, distance et temps de trajet.

    Contexte : La Corse est desservie par plusieurs compagnies maritimes
    (Corsica Ferries, La Méridionale, Corsica Linea) reliant l'île au continent
    et assurant les liaisons inter-îles.
    """
    gen = tg.MathsGenerator(seed)

    # Ports corses avec coordonnées (latitude, longitude) approximatives
    ports = {
        "Ajaccio": {"lat": 41.92, "lon": 8.74, "desc": "Capitale, principal port de commerce"},
        "Bastia": {"lat": 42.70, "lon": 9.45, "desc": "Porte d'entrée du Cap Corse"},
        "Calvi": {"lat": 42.57, "lon": 8.76, "desc": "Port de la Balagne"},
        "L'Île-Rousse": {"lat": 42.64, "lon": 8.94, "desc": "Port créé par Pascal Paoli"},
        "Porto-Vecchio": {"lat": 41.59, "lon": 9.28, "desc": "Port du Sud, plages paradisiaques"},
        "Bonifacio": {"lat": 41.39, "lon": 9.16, "desc": "Cité des falaises, face à la Sardaigne"},
        "Propriano": {"lat": 41.68, "lon": 8.90, "desc": "Port du Valinco"},
    }

    # Sélection aléatoire de deux ports différents
    port_names = list(ports.keys())
    depart = gen.random_element_from(port_names)
    arrivee = depart
    while arrivee == depart:
        arrivee = gen.random_element_from(port_names)

    # Conditions météo
    vents = [
        {"nom": "Libeccio", "direction": 225, "force": gen.random_integer(15, 35)},
        {"nom": "Tramontane", "direction": 315, "force": gen.random_integer(20, 40)},
        {"nom": "Levante", "direction": 90, "force": gen.random_integer(10, 25)},
        {"nom": "Ponente", "direction": 270, "force": gen.random_integer(15, 30)},
    ]
    vent = gen.random_element_from(vents)

    # Vitesse du navire (en nœuds)
    vitesse_navire = gen.random_integer(15, 25)

    # Type de navire
    navires = [
        {"type": "Ferry rapide", "capacite": 700, "longueur": 175},
        {"type": "Cargo mixte", "capacite": 500, "longueur": 150},
        {"type": "NGV (Navire Grande Vitesse)", "capacite": 450, "longueur": 100},
    ]
    navire = gen.random_element_from(navires)

    return {
        "port_depart": depart,
        "port_arrivee": arrivee,
        "coords_depart": ports[depart],
        "coords_arrivee": ports[arrivee],
        "vent": vent,
        "vitesse_navire": tm.Integer(n=vitesse_navire),
        "navire": navire,
    }


def solve(
    *, port_depart, port_arrivee, coords_depart, coords_arrivee, vent, vitesse_navire, navire
):
    """
    Résout le problème de navigation maritime.
    Calcule la distance orthodromique, le cap et le temps de trajet.
    """

    # Conversion des coordonnées en radians
    lat1 = math.radians(coords_depart["lat"])
    lon1 = math.radians(coords_depart["lon"])
    lat2 = math.radians(coords_arrivee["lat"])
    lon2 = math.radians(coords_arrivee["lon"])

    # Calcul de la distance orthodromique (formule de Haversine)
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))

    # Rayon de la Terre en km
    R = 6371
    distance_km = R * c

    # Conversion en milles nautiques (1 mille nautique = 1.852 km)
    distance_nm = distance_km / 1.852

    # Calcul du cap initial (bearing)
    y = math.sin(lon2 - lon1) * math.cos(lat2)
    x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(lon2 - lon1)
    cap_rad = math.atan2(y, x)
    cap_degres = (math.degrees(cap_rad) + 360) % 360

    # Effet du vent sur la vitesse
    # Angle entre le cap et la direction du vent
    angle_vent = abs(cap_degres - vent["direction"])
    if angle_vent > 180:
        angle_vent = 360 - angle_vent

    # Calcul de l'effet du vent
    vent_favorable = math.cos(math.radians(angle_vent))
    vitesse_effective = vitesse_navire.n + (vent["force"] * vent_favorable * 0.1)

    # Temps de trajet
    temps_heures = distance_nm / vitesse_effective
    heures = int(temps_heures)
    minutes = int((temps_heures - heures) * 60)

    # Consommation de carburant (approximative)
    consommation_par_mille = 50  # litres par mille nautique
    carburant_total = distance_nm * consommation_par_mille

    return {
        "distance_km": round(distance_km, 1),
        "distance_nm": round(distance_nm, 1),
        "cap_degres": round(cap_degres, 1),
        "cap_cardinal": degres_vers_cardinal(cap_degres),
        "vitesse_effective": round(vitesse_effective, 1),
        "temps_heures": heures,
        "temps_minutes": minutes,
        "carburant_litres": round(carburant_total, 0),
        "effet_vent": "Favorable" if vent_favorable > 0 else "Défavorable",
    }


def degres_vers_cardinal(degres):
    """Convertit un cap en degrés vers une direction cardinale."""
    directions = [
        "N",
        "NNE",
        "NE",
        "ENE",
        "E",
        "ESE",
        "SE",
        "SSE",
        "S",
        "SSO",
        "SO",
        "OSO",
        "O",
        "ONO",
        "NO",
        "NNO",
    ]
    index = round(degres / 22.5) % 16
    return directions[index]


def create_svg_map(components, solution):
    """
    Crée une carte SVG montrant la route maritime.
    """
    # Positions simplifiées pour la visualisation
    positions = {
        "Ajaccio": (120, 200),
        "Bastia": (180, 80),
        "Calvi": (130, 100),
        "L'Île-Rousse": (145, 90),
        "Porto-Vecchio": (185, 280),
        "Bonifacio": (175, 320),
        "Propriano": (135, 230),
    }

    depart_pos = positions[components["port_depart"]]
    arrivee_pos = positions[components["port_arrivee"]]

    svg = f"""
    <svg viewBox="0 0 300 400" xmlns="http://www.w3.org/2000/svg">
        <!-- Titre -->
        <text x="150" y="20" text-anchor="middle" font-size="14" font-weight="bold">
            Navigation {components["port_depart"]} → {components["port_arrivee"]}
        </text>
        
        <!-- Mer -->
        <rect width="300" height="400" fill="#E6F3FF"/>
        
        <!-- Forme simplifiée de la Corse -->
        <path d="M 150 50 Q 180 60, 190 100 L 195 150 Q 200 200, 185 250 
                 L 170 320 Q 160 360, 150 380 Q 140 360, 130 320 
                 L 115 250 Q 100 200, 105 150 L 110 100 Q 120 60, 150 50 Z"
              fill="#90EE90" stroke="#228B22" stroke-width="2"/>
        
        <!-- Ports -->
        {
        "".join(
            [
                f'''
        <circle cx="{pos[0]}" cy="{pos[1]}" r="3" 
                fill="{"red" if port in [components["port_depart"], components["port_arrivee"]] else "gray"}"/>
        <text x="{pos[0] + 10}" y="{pos[1]}" font-size="9">{port}</text>
        '''
                for port, pos in positions.items()
            ]
        )
    }
        
        <!-- Route maritime -->
        <line x1="{depart_pos[0]}" y1="{depart_pos[1]}" 
              x2="{arrivee_pos[0]}" y2="{arrivee_pos[1]}"
              stroke="blue" stroke-width="2" stroke-dasharray="5,5"
              marker-end="url(#arrowhead)"/>
        
        <!-- Flèche -->
        <defs>
            <marker id="arrowhead" markerWidth="10" markerHeight="7" 
                    refX="10" refY="3.5" orient="auto">
                <polygon points="0 0, 10 3.5, 0 7" fill="blue"/>
            </marker>
        </defs>
        
        <!-- Indicateur de vent -->
        <g transform="translate(250, 100)">
            <circle r="25" fill="none" stroke="black" stroke-width="1"/>
            <line x1="0" y1="0" 
                  x2="{25 * math.cos(math.radians(components["vent"]["direction"] - 90))}" 
                  y2="{25 * math.sin(math.radians(components["vent"]["direction"] - 90))}"
                  stroke="red" stroke-width="2" marker-end="url(#wind)"/>
            <text x="0" y="-30" text-anchor="middle" font-size="10">
                {components["vent"]["nom"]}
            </text>
            <text x="0" y="40" text-anchor="middle" font-size="9">
                {components["vent"]["force"]} nœuds
            </text>
        </g>
        
        <defs>
            <marker id="wind" markerWidth="8" markerHeight="6" 
                    refX="8" refY="3" orient="auto">
                <polygon points="0 0, 8 3, 0 6" fill="red"/>
            </marker>
        </defs>
        
        <!-- Informations de navigation -->
        <rect x="10" y="350" width="120" height="40" fill="white" opacity="0.9" stroke="black"/>
        <text x="15" y="365" font-size="10">Distance: {solution["distance_nm"]} NM</text>
        <text x="15" y="375" font-size="10">Cap: {solution["cap_degres"]}° ({
        solution["cap_cardinal"]
    })</text>
        <text x="15" y="385" font-size="10">Durée: {
        solution["temps_heures"]
    }h{solution["temps_minutes"]:02d}</text>
    </svg>
    """
    return svg


def generate_python_code(components, solution):
    """
    Génère le code Python pour que les élèves puissent vérifier leurs calculs.
    """
    code = f"""
import math
import matplotlib.pyplot as plt
import numpy as np

# Données de navigation
depart = "{components["port_depart"]}"
arrivee = "{components["port_arrivee"]}"
coords_depart = {components["coords_depart"]}
coords_arrivee = {components["coords_arrivee"]}

# Fonction de calcul de distance orthodromique
def distance_orthodromique(lat1, lon1, lat2, lon2):
    \"\"\"
    Calcule la distance entre deux points sur une sphère.
    Utilisé pour la navigation maritime et aérienne.
    \"\"\"
    # Conversion en radians
    lat1, lon1 = math.radians(lat1), math.radians(lon1)
    lat2, lon2 = math.radians(lat2), math.radians(lon2)
    
    # Formule de Haversine
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    # Distance en km (rayon terrestre = 6371 km)
    distance_km = 6371 * c
    
    # Conversion en milles nautiques
    distance_nm = distance_km / 1.852
    
    return distance_km, distance_nm

# Fonction de calcul du cap
def calculer_cap(lat1, lon1, lat2, lon2):
    \"\"\"
    Calcule le cap initial pour aller d'un point à un autre.
    \"\"\"
    lat1, lon1 = math.radians(lat1), math.radians(lon1)
    lat2, lon2 = math.radians(lat2), math.radians(lon2)
    
    y = math.sin(lon2 - lon1) * math.cos(lat2)
    x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(lon2 - lon1)
    cap_rad = math.atan2(y, x)
    cap_degres = (math.degrees(cap_rad) + 360) % 360
    
    return cap_degres

# Calculs
distance_km, distance_nm = distance_orthodromique(
    coords_depart['lat'], coords_depart['lon'],
    coords_arrivee['lat'], coords_arrivee['lon']
)

cap = calculer_cap(
    coords_depart['lat'], coords_depart['lon'],
    coords_arrivee['lat'], coords_arrivee['lon']
)

# Effet du vent
vent_direction = {components["vent"]["direction"]}
vent_force = {components["vent"]["force"]}
angle_vent = abs(cap - vent_direction)
if angle_vent > 180:
    angle_vent = 360 - angle_vent

effet_vent = math.cos(math.radians(angle_vent))
vitesse_base = {components["vitesse_navire"].n}
vitesse_effective = vitesse_base + (vent_force * effet_vent * 0.1)

# Temps de trajet
temps_heures = distance_nm / vitesse_effective

# Affichage des résultats
print("⚓ NAVIGATION MARITIME EN CORSE")
print("=" * 40)
print(f"Route: {{depart}} → {{arrivee}}")
print(f"Distance: {{distance_km:.1f}} km ({{distance_nm:.1f}} milles nautiques)")
print(f"Cap à suivre: {{cap:.1f}}°")
print(f"Vitesse effective: {{vitesse_effective:.1f}} nœuds")
print(f"Temps de trajet: {{int(temps_heures)}}h{{int((temps_heures % 1) * 60):02d}}")
print(f"\\nConditions: {components["vent"]["nom"]} {{vent_force}} nœuds")
print(f"Navire: {components["navire"]["type"]}")

# Visualisation graphique
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Carte de navigation
ax1.set_title(f"Route maritime {{depart}} → {{arrivee}}", fontweight='bold')
ax1.set_xlabel("Longitude")
ax1.set_ylabel("Latitude")

# Tracer la côte corse (simplifié)
corse_lon = [8.5, 9.0, 9.5, 9.5, 9.0, 8.5, 8.5]
corse_lat = [41.3, 41.3, 41.8, 42.8, 42.8, 42.3, 41.3]
ax1.plot(corse_lon, corse_lat, 'g-', linewidth=2, label='Corse')
ax1.fill(corse_lon, corse_lat, color='lightgreen', alpha=0.5)

# Points et route
ax1.plot(coords_depart['lon'], coords_depart['lat'], 'ro', markersize=10, label=depart)
ax1.plot(coords_arrivee['lon'], coords_arrivee['lat'], 'bo', markersize=10, label=arrivee)
ax1.plot([coords_depart['lon'], coords_arrivee['lon']], 
         [coords_depart['lat'], coords_arrivee['lat']], 
         'b--', linewidth=2, label='Route')

# Vecteur vent
wind_scale = 0.3
wind_x = wind_scale * math.cos(math.radians(vent_direction - 90))
wind_y = wind_scale * math.sin(math.radians(vent_direction - 90))
ax1.arrow(9.0, 42.5, wind_x, wind_y, head_width=0.05, 
          head_length=0.05, fc='red', ec='red', label=f'Vent: {components["vent"]["nom"]}')

ax1.legend()
ax1.grid(True, alpha=0.3)
ax1.set_aspect('equal')

# Profil de vitesse
ax2.set_title("Analyse de la traversée", fontweight='bold')
ax2.set_xlabel("Temps (heures)")
ax2.set_ylabel("Distance parcourue (NM)")

temps = np.linspace(0, temps_heures, 100)
distance_parcourue = vitesse_effective * temps

ax2.plot(temps, distance_parcourue, 'b-', linewidth=2, label='Progression')
ax2.axhline(y=distance_nm, color='r', linestyle='--', label=f'Distance totale: {{distance_nm:.1f}} NM')
ax2.fill_between(temps, 0, distance_parcourue, alpha=0.3)

# Annotations
ax2.text(temps_heures/2, distance_nm/2, 
         f'Vitesse: {{vitesse_effective:.1f}} nœuds\\n' +
         f'Effet vent: {{"Favorable" if effet_vent > 0 else "Défavorable"}}',
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

ax2.legend()
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# Questions supplémentaires
print("\\n📝 QUESTIONS D'APPROFONDISSEMENT:")
print("1. Quelle serait la consommation de carburant pour ce trajet ?")
print(f"   (Base: 50 L/NM) → Réponse: {{distance_nm * 50:.0f}} litres")
print("2. À quelle heure faut-il partir pour arriver avant 18h ?")
print(f"   → Départ au plus tard à {{18 - int(temps_heures):02d}}h{{60 - int((temps_heures % 1) * 60):02d}}")
print("3. Quel serait l'impact d'un vent de face de 30 nœuds ?")
"""

    return code


def generate_question_text(components):
    """
    Génère le texte de la question avec contexte maritime corse.
    """
    return f"""
    ⚓ **Exercice : Navigation maritime en Corse**
    
    Vous êtes officier de navigation sur un {components["navire"]["type"]} de la compagnie 
    Corsica Ferries. Vous devez planifier la traversée de **{components["port_depart"]}** 
    ({components["coords_depart"]["desc"]}) vers **{components["port_arrivee"]}** 
    ({components["coords_arrivee"]["desc"]}).
    
    **Données de navigation :**
    - Coordonnées {components["port_depart"]} : {components["coords_depart"]["lat"]}°N, {components["coords_depart"]["lon"]}°E
    - Coordonnées {components["port_arrivee"]} : {components["coords_arrivee"]["lat"]}°N, {components["coords_arrivee"]["lon"]}°E
    - Vitesse du navire : {components["vitesse_navire"]} nœuds
    - Vent : {components["vent"]["nom"]} de {components["vent"]["force"]} nœuds, direction {components["vent"]["direction"]}°
    - Capacité du navire : {components["navire"]["capacite"]} passagers
    
    **Questions :**
    
    **Partie A - Calculs de base**
    1. Calculez la distance orthodromique entre les deux ports (en km et en milles nautiques)
    2. Déterminez le cap initial à suivre (en degrés et direction cardinale)
    3. Calculez le temps de traversée en tenant compte du vent
    
    **Partie B - Analyse vectorielle**
    1. Représentez la route comme un vecteur dans le plan
    2. Décomposez le vecteur vent et calculez son effet sur la vitesse
    3. Déterminez la dérive due au vent
    
    **Partie C - Optimisation**
    1. À quelle heure faut-il partir pour arriver à 16h00 ?
    2. Quelle route alternative minimiserait l'effet du vent ?
    3. Calculez la consommation de carburant (base : 50 L/mille nautique)
    
    **Contexte historique :**
    Les liaisons maritimes sont vitales pour la Corse. Pascal Paoli créa le port de 
    L'Île-Rousse en 1765 pour concurrencer les ports génois de Calvi et Algajola.
    Aujourd'hui, plus de 8 millions de passagers transitent annuellement par les ports corses.
    
    **Formules utiles :**
    - Distance orthodromique : d = R × arccos(sin(φ₁)×sin(φ₂) + cos(φ₁)×cos(φ₂)×cos(Δλ))
    - Cap initial : θ = atan2(sin(Δλ)×cos(φ₂), cos(φ₁)×sin(φ₂) − sin(φ₁)×cos(φ₂)×cos(Δλ))
    - Où R = 6371 km (rayon terrestre), φ = latitude, λ = longitude
    """
