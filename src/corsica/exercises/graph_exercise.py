"""
Exercice de graphiques : Analyse du tourisme en Corse
Pour le niveau seconde - Statistiques et représentations graphiques
"""

import teachers.generator as tg
from teachers.defaults import SEED


def generate_components(difficulty, seed=SEED) -> dict:
    """
    Génère un exercice d'analyse de données touristiques corses.
    L'élève doit analyser et représenter graphiquement les données.

    Contexte : La Corse accueille environ 3 millions de touristes par an,
    avec des variations saisonnières importantes.
    """
    gen = tg.MathsGenerator(seed)

    # Données touristiques par mois (en milliers de visiteurs)
    # Basées sur des statistiques réelles de la Corse
    mois = ["Jan", "Fév", "Mar", "Avr", "Mai", "Juin", "Juil", "Août", "Sep", "Oct", "Nov", "Déc"]

    # Génération de données réalistes avec variations
    base_visitors = [
        gen.random_integer(15, 25),  # Janvier
        gen.random_integer(18, 28),  # Février
        gen.random_integer(35, 50),  # Mars
        gen.random_integer(80, 120),  # Avril
        gen.random_integer(150, 200),  # Mai
        gen.random_integer(280, 350),  # Juin
        gen.random_integer(450, 550),  # Juillet
        gen.random_integer(500, 600),  # Août
        gen.random_integer(200, 250),  # Septembre
        gen.random_integer(100, 150),  # Octobre
        gen.random_integer(40, 60),  # Novembre
        gen.random_integer(25, 35),  # Décembre
    ]

    # Répartition par région (en pourcentage)
    regions = {
        "Ajaccio": gen.random_integer(25, 35),
        "Bastia": gen.random_integer(20, 30),
        "Porto-Vecchio": gen.random_integer(15, 25),
        "Calvi": gen.random_integer(10, 20),
        "Corte": gen.random_integer(5, 10),
    }

    # Ajuster pour que le total fasse 100%
    total = sum(regions.values())
    regions = {k: round(v * 100 / total) for k, v in regions.items()}

    # Types d'hébergement
    hebergements = {
        "Hôtels": gen.random_integer(35, 45),
        "Locations": gen.random_integer(25, 35),
        "Campings": gen.random_integer(15, 25),
        "Chambres d'hôtes": gen.random_integer(10, 15),
        "Autres": gen.random_integer(5, 10),
    }

    # Ajuster pour 100%
    total_h = sum(hebergements.values())
    hebergements = {k: round(v * 100 / total_h) for k, v in hebergements.items()}

    return {
        "mois": mois,
        "visiteurs": base_visitors,
        "regions": regions,
        "hebergements": hebergements,
        "annee": gen.random_integer(2020, 2024),
    }


def solve(*, mois, visiteurs, regions, hebergements, annee):
    """
    Calcule les statistiques demandées.
    """
    # Calcul du total annuel
    total_annuel = sum(visiteurs)

    # Moyenne mensuelle
    moyenne_mensuelle = total_annuel / 12

    # Identification de la haute saison
    max_visiteurs = max(visiteurs)
    mois_pic = mois[visiteurs.index(max_visiteurs)]

    # Identification de la basse saison
    min_visiteurs = min(visiteurs)
    mois_creux = mois[visiteurs.index(min_visiteurs)]

    # Calcul de la médiane
    visiteurs_tries = sorted(visiteurs)
    mediane = (visiteurs_tries[5] + visiteurs_tries[6]) / 2

    # Calcul de l'écart-type
    variance = sum((x - moyenne_mensuelle) ** 2 for x in visiteurs) / 12
    ecart_type = variance**0.5

    return {
        "total_annuel": total_annuel * 1000,  # Conversion en nombre réel
        "moyenne_mensuelle": round(moyenne_mensuelle, 2),
        "mediane": mediane,
        "ecart_type": round(ecart_type, 2),
        "mois_pic": mois_pic,
        "max_visiteurs": max_visiteurs,
        "mois_creux": mois_creux,
        "min_visiteurs": min_visiteurs,
        "ratio_haute_basse": round(max_visiteurs / min_visiteurs, 1),
    }


def create_matplotlib_code(components):
    """
    Génère le code Python/matplotlib pour créer les graphiques.
    """
    code = f"""
import matplotlib.pyplot as plt
import numpy as np

# Données touristiques de la Corse pour l'année {components["annee"]}
mois = {components["mois"]}
visiteurs = {components["visiteurs"]}  # en milliers

# Configuration du style
plt.style.use('seaborn-v0_8-darkgrid')
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle(f"Analyse du tourisme en Corse - Année {components["annee"]}", fontsize=16, fontweight='bold')

# 1. Graphique en barres - Visiteurs par mois
ax1 = axes[0, 0]
colors = ['#FF6B6B' if v > 400 else '#4ECDC4' if v > 200 else '#95E1D3' for v in visiteurs]
bars = ax1.bar(mois, visiteurs, color=colors, edgecolor='black', linewidth=1)
ax1.set_xlabel('Mois', fontsize=12)
ax1.set_ylabel('Visiteurs (milliers)', fontsize=12)
ax1.set_title('Fréquentation touristique mensuelle', fontsize=14)
ax1.grid(axis='y', alpha=0.3)

# Ajouter une ligne de moyenne
moyenne = np.mean(visiteurs)
ax1.axhline(y=moyenne, color='red', linestyle='--', label=f'Moyenne: {{moyenne:.0f}}k')
ax1.legend()

# 2. Graphique circulaire - Répartition par région
ax2 = axes[0, 1]
regions = {list(components["regions"].items())}
region_names = [r[0] for r in regions]
region_values = [r[1] for r in regions]
colors_regions = ['#FF9999', '#66B2FF', '#99FF99', '#FFD700', '#FF99FF']
wedges, texts, autotexts = ax2.pie(region_values, labels=region_names, colors=colors_regions, 
                                     autopct='%1.1f%%', startangle=90)
ax2.set_title('Répartition des touristes par région', fontsize=14)

# 3. Courbe d'évolution - Tendance saisonnière
ax3 = axes[1, 0]
x = np.arange(len(mois))
ax3.plot(x, visiteurs, 'b-', linewidth=2, marker='o', markersize=6, label='Visiteurs')
ax3.fill_between(x, visiteurs, alpha=0.3)
ax3.set_xlabel('Mois', fontsize=12)
ax3.set_ylabel('Visiteurs (milliers)', fontsize=12)
ax3.set_title('Évolution saisonnière du tourisme', fontsize=14)
ax3.set_xticks(x)
ax3.set_xticklabels(mois, rotation=45)
ax3.grid(True, alpha=0.3)

# Annotations pour les pics
max_idx = visiteurs.index(max(visiteurs))
min_idx = visiteurs.index(min(visiteurs))
ax3.annotate(f'Pic: {{visiteurs[max_idx]}}k', xy=(max_idx, visiteurs[max_idx]), 
             xytext=(max_idx, visiteurs[max_idx] + 50),
             arrowprops=dict(arrowstyle='->', color='red'))
ax3.annotate(f'Creux: {{visiteurs[min_idx]}}k', xy=(min_idx, visiteurs[min_idx]), 
             xytext=(min_idx, visiteurs[min_idx] - 50),
             arrowprops=dict(arrowstyle='->', color='blue'))

# 4. Graphique en barres horizontales - Types d'hébergement
ax4 = axes[1, 1]
hebergements = {list(components["hebergements"].items())}
heberg_names = [h[0] for h in hebergements]
heberg_values = [h[1] for h in hebergements]
colors_heberg = plt.cm.Set3(np.linspace(0, 1, len(heberg_names)))
bars = ax4.barh(heberg_names, heberg_values, color=colors_heberg)
ax4.set_xlabel('Pourcentage (%)', fontsize=12)
ax4.set_title('Répartition par type d\\'hébergement', fontsize=14)
ax4.grid(axis='x', alpha=0.3)

# Ajouter les valeurs sur les barres
for bar, value in zip(bars, heberg_values):
    ax4.text(value + 1, bar.get_y() + bar.get_height()/2, f'{{value}}%', 
             va='center', fontsize=10)

plt.tight_layout()
plt.show()

# Calculs statistiques
total_annuel = sum(visiteurs) * 1000
print(f"\\n📊 Statistiques touristiques de la Corse - {components["annee"]}")
print(f"{"=" * 50}")
print(f"Total annuel : {{total_annuel:,.0f}} visiteurs")
print(f"Moyenne mensuelle : {{np.mean(visiteurs):.1f}} milliers")
print(f"Médiane : {{np.median(visiteurs):.1f}} milliers")
print(f"Écart-type : {{np.std(visiteurs):.1f}} milliers")
print(f"Mois le plus fréquenté : {{mois[max_idx]}} ({{max(visiteurs)}} milliers)")
print(f"Mois le moins fréquenté : {{mois[min_idx]}} ({{min(visiteurs)}} milliers)")
print(f"Ratio haute/basse saison : {{max(visiteurs)/min(visiteurs):.1f}}x")
"""
    return code


def generate_question_text(components):
    """
    Génère le texte de la question avec contexte culturel.
    """
    return f"""
    📊 **Exercice : Analyse du tourisme en Corse**
    
    L'Agence du Tourisme de la Corse (ATC) vous demande d'analyser les données 
    de fréquentation touristique pour l'année {components["annee"]}.
    
    **Données fournies :**
    - Nombre de visiteurs par mois (en milliers)
    - Répartition géographique des touristes
    - Types d'hébergement préférés
    
    **Partie A - Calculs statistiques**
    1. Calculez le nombre total de touristes sur l'année
    2. Déterminez la moyenne et la médiane mensuelles
    3. Calculez l'écart-type pour mesurer la variabilité saisonnière
    4. Identifiez les mois de haute et basse saison
    
    **Partie B - Représentations graphiques**
    1. Créez un histogramme de la fréquentation mensuelle
    2. Réalisez un diagramme circulaire de la répartition par région
    3. Tracez la courbe d'évolution saisonnière
    4. Représentez la répartition des types d'hébergement
    
    **Partie C - Analyse et interprétation**
    1. Commentez la saisonnalité du tourisme corse
    2. Proposez des recommandations pour lisser la fréquentation
    3. Identifiez les régions à fort potentiel de développement
    
    **Contexte culturel :**
    Le tourisme représente environ 35% du PIB de la Corse et emploie
    directement ou indirectement 30 000 personnes sur l'île.
    """
