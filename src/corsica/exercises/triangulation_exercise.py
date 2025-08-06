"""
Exercice de triangulation : Localisation des tours génoises de Corse
Pour le niveau seconde - Trigonométrie et géométrie
"""

import teachers.generator as tg
import teachers.maths as tm
from teachers.defaults import SEED
import math


def generate_components(difficulty, seed=SEED) -> dict:
    """
    Génère un exercice de triangulation basé sur les tours génoises de Corse.
    L'élève doit localiser une tour en utilisant deux points d'observation.

    Contexte historique : Les tours génoises sont des monuments emblématiques
    de la Corse, construites entre le XVe et XVIIe siècle pour surveiller
    les côtes contre les invasions barbaresques.

    >>> generate_components(None, 0)
    """
    gen = tg.MathsGenerator(seed)

    # Tours génoises célèbres de Corse avec leurs coordonnées approximatives
    tours = [
        {"nom": "Tour de la Parata", "lieu": "Ajaccio", "lat": 41.9, "lon": 8.6},
        {"nom": "Tour de Campomoro", "lieu": "Propriano", "lat": 41.6, "lon": 8.8},
        {"nom": "Tour de Porto", "lieu": "Porto", "lat": 42.3, "lon": 8.7},
        {"nom": "Tour de Nonza", "lieu": "Cap Corse", "lat": 42.8, "lon": 9.3},
        {"nom": "Tour de l'Osse", "lieu": "Cargèse", "lat": 42.1, "lon": 8.6},
    ]

    tour = gen.random_element_from(tours)

    # Points d'observation (villages ou villes corses)
    observer1_distance = gen.random_integer(5, 15)  # km
    observer2_distance = gen.random_integer(8, 18)  # km

    # Angles d'observation (en degrés)
    angle1 = gen.random_integer(20, 70)
    angle2 = gen.random_integer(30, 80)

    # Distance entre les deux observateurs
    base_distance = gen.random_integer(10, 25)  # km

    return {
        "tour": tour,
        "observer1_distance": tm.Integer(n=observer1_distance),
        "observer2_distance": tm.Integer(n=observer2_distance),
        "angle1": tm.Integer(n=angle1),
        "angle2": tm.Integer(n=angle2),
        "base_distance": tm.Integer(n=base_distance),
    }


def solve(*, tour, observer1_distance, observer2_distance, angle1, angle2, base_distance):
    """
    Résout le problème de triangulation.
    Utilise la loi des sinus et des cosinus pour déterminer la position.
    """
    # Conversion des angles en radians pour les calculs
    angle1_rad = math.radians(angle1.n)
    angle2_rad = math.radians(angle2.n)

    # Calcul de l'angle au sommet (tour)
    angle_tour = 180 - angle1.n - angle2.n
    angle_tour_rad = math.radians(angle_tour)

    # Utilisation de la loi des sinus
    # base_distance / sin(angle_tour) = d1 / sin(angle2) = d2 / sin(angle1)

    calculated_d1 = (base_distance.n * math.sin(angle2_rad)) / math.sin(angle_tour_rad)
    calculated_d2 = (base_distance.n * math.sin(angle1_rad)) / math.sin(angle_tour_rad)

    # Vérification avec les distances données
    error_margin = 0.5  # km

    return {
        "maths_object": tm.Integer(n=angle_tour),
        "angle_tour": angle_tour,
        "calculated_distance1": round(calculated_d1, 2),
        "calculated_distance2": round(calculated_d2, 2),
        "tour_info": tour,
        "method": "Triangulation par la loi des sinus",
    }


def create_svg_diagram(components):
    """
    Crée un diagramme SVG pour visualiser le problème de triangulation.
    """
    svg = f"""
    <svg viewBox="0 0 400 300" xmlns="http://www.w3.org/2000/svg">
        <!-- Titre -->
        <text x="200" y="20" text-anchor="middle" font-size="14" font-weight="bold">
            Localisation de {components["tour"]["nom"]} - {components["tour"]["lieu"]}
        </text>
        
        <!-- Points d'observation -->
        <circle cx="100" cy="250" r="5" fill="blue"/>
        <text x="100" y="270" text-anchor="middle" font-size="12">Observateur 1</text>
        
        <circle cx="300" cy="250" r="5" fill="blue"/>
        <text x="300" y="270" text-anchor="middle" font-size="12">Observateur 2</text>
        
        <!-- Tour génoise -->
        <rect x="195" y="80" width="10" height="30" fill="#8B4513"/>
        <polygon points="200,70 190,80 210,80" fill="#8B4513"/>
        <text x="200" y="60" text-anchor="middle" font-size="12" font-weight="bold">
            {components["tour"]["nom"]}
        </text>
        
        <!-- Lignes de visée -->
        <line x1="100" y1="250" x2="200" y2="110" stroke="red" stroke-width="1" stroke-dasharray="5,5"/>
        <line x1="300" y1="250" x2="200" y2="110" stroke="red" stroke-width="1" stroke-dasharray="5,5"/>
        <line x1="100" y1="250" x2="300" y2="250" stroke="black" stroke-width="2"/>
        
        <!-- Angles -->
        <text x="120" y="240" font-size="12">{components["angle1"]}°</text>
        <text x="270" y="240" font-size="12">{components["angle2"]}°</text>
        
        <!-- Distance de base -->
        <text x="200" y="265" text-anchor="middle" font-size="12">
            {components["base_distance"]} km
        </text>
        
        <!-- Légende -->
        <text x="10" y="30" font-size="10" fill="gray">
            Méthode de triangulation utilisée par les géomètres corses
        </text>
    </svg>
    """
    return svg


def generate_question_text(components):
    """
    Génère le texte de la question en français avec contexte culturel.
    """
    return f"""
    📍 **Exercice : Localisation d'une tour génoise**
    
    Vous êtes un géomètre travaillant pour le Conservatoire du littoral de Corse.
    Vous devez localiser précisément la {components["tour"]["nom"]} située près de {components["tour"]["lieu"]}.
    
    Deux observateurs sont positionnés à {components["base_distance"]} km l'un de l'autre.
    - L'observateur 1 mesure un angle de {components["angle1"]}° avec la ligne de base
    - L'observateur 2 mesure un angle de {components["angle2"]}° avec la ligne de base
    
    **Questions :**
    1. Calculez l'angle au sommet (à la tour) du triangle formé
    2. En utilisant la loi des sinus, déterminez les distances de chaque observateur à la tour
    3. Vérifiez vos calculs sachant que les distances mesurées au GPS sont d'environ:
       - Observateur 1 à la tour : {components["observer1_distance"]} km
       - Observateur 2 à la tour : {components["observer2_distance"]} km
    
    **Bonus culturel :** Cette tour fait partie des 85 tours génoises 
    qui jalonnent le littoral corse sur 500 km de côtes.
    """
