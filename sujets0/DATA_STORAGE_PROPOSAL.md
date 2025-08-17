# Proposition de Stockage des Données de Compétences

Ce document propose une approche structurée pour stocker et gérer les données de mapping entre les générateurs de questions et les compétences.

## Options de Stockage

### 1. Fichier JSON dédié (Recommandé)

**Structure proposée** : `sujets0/competences_data.json`

```json
{
  "metadata": {
    "version": "1.0",
    "last_updated": "2024-01-15",
    "description": "Mapping des générateurs aux compétences BAC 1ère",
    "total_generators": 24,
    "total_competences": 41
  },
  "competences_definitions": {
    "bac_1_auto_1_2DE": "Comparer, ranger, encadrer des nombres réels",
    "bac_1_auto_2_2DE": "Effectuer des calculs sur fractions, puissances, racines",
    "bac_1_auto_3_2DE": "Utiliser les puissances d'exposant entier",
    "...": "..."
  },
  "generators_mapping": {
    "spe_sujet1_auto_01_question.py": {
      "competences": ["bac_1_auto_2_2DE", "bac_1_auto_4_2DE", "bac_1_auto_8_2DE"],
      "title": "Calcul d'inverse de multiple",
      "difficulty": "facile",
      "domains": ["calcul_numerique", "fractions"],
      "estimated_time_minutes": 3
    },
    "spe_sujet1_auto_02_question.py": {
      "competences": ["bac_1_auto_2_2DE", "bac_1_auto_8_2DE", "bac_1_auto_12_2DE"],
      "title": "Évaluation d'expression fractionnaire",
      "difficulty": "moyen",
      "domains": ["calcul_numerique", "calcul_litteral"],
      "estimated_time_minutes": 5
    }
  },
  "statistics": {
    "competences_frequency": {
      "bac_1_auto_17_2DE": 6,
      "bac_1_auto_9_2DE": 4,
      "bac_1_auto_24_2DE": 4
    },
    "domains_coverage": {
      "calcul_numerique": 8,
      "fonctions": 6,
      "probabilites": 4,
      "geometrie": 3
    }
  }
}
```

**Avantages** :
- ✅ Structure claire et extensible
- ✅ Facile à parser en Python avec `json.load()`
- ✅ Support des métadonnées et statistiques
- ✅ Validation possible avec JSON Schema
- ✅ Lisible par les humains

**Inconvénients** :
- ❌ Redondance potentielle
- ❌ Pas de requêtes complexes natives

### 2. Base de données SQLite

**Structure proposée** : `sujets0/competences.db`

```sql
-- Table des compétences
CREATE TABLE competences (
    id TEXT PRIMARY KEY,
    description TEXT,
    domain TEXT,
    level TEXT
);

-- Table des générateurs
CREATE TABLE generators (
    filename TEXT PRIMARY KEY,
    title TEXT,
    difficulty TEXT,
    estimated_time INTEGER
);

-- Table de liaison (many-to-many)
CREATE TABLE generator_competences (
    generator_filename TEXT,
    competence_id TEXT,
    weight REAL DEFAULT 1.0,
    FOREIGN KEY (generator_filename) REFERENCES generators(filename),
    FOREIGN KEY (competence_id) REFERENCES competences(id)
);
```

**Avantages** :
- ✅ Requêtes SQL puissantes
- ✅ Pas de redondance
- ✅ Relations normalisées
- ✅ Performance pour grandes données

**Inconvénients** :
- ❌ Plus complexe à maintenir
- ❌ Dépendance SQLite
- ❌ Moins lisible par les humains

### 3. Fichiers YAML séparés

**Structure proposée** :
```
sujets0/
├── competences/
│   ├── definitions.yml
│   ├── spe_sujet1_mapping.yml
│   └── spe_sujet2_mapping.yml
```

**Avantages** :
- ✅ Très lisible
- ✅ Modularité
- ✅ Commentaires intégrés

**Inconvénients** :
- ❌ Fragmentation des données
- ❌ Synchronisation manuelle

### 4. Intégration dans le code Python

**Structure proposée** : `sujets0/competences_config.py`

```python
COMPETENCES_MAPPING = {
    "spe_sujet1_auto_01_question.py": {
        "competences": ["bac_1_auto_2_2DE", "bac_1_auto_4_2DE", "bac_1_auto_8_2DE"],
        "metadata": {...}
    }
}

COMPETENCES_DEFINITIONS = {
    "bac_1_auto_1_2DE": "Comparer, ranger, encadrer des nombres réels",
    # ...
}
```

**Avantages** :
- ✅ Import direct en Python
- ✅ Validation à l'exécution
- ✅ Pas de parsing externe

**Inconvénients** :
- ❌ Moins flexible
- ❌ Modification = redéploiement

## Recommandation : Approche JSON

Je recommande l'**option 1 (JSON)** pour les raisons suivantes :

1. **Équilibre optimal** entre simplicité et fonctionnalité
2. **Extensibilité** : facile d'ajouter des champs
3. **Interopérabilité** : utilisable par d'autres langages
4. **Maintenance** : éditable manuellement si nécessaire
5. **Performance** : suffisante pour nos besoins actuels

## Plan d'Implémentation

### Phase 1 : Structure de base

```python
# sujets0/competences_manager.py
import json
from pathlib import Path
from typing import Dict, List, Optional

class CompetencesManager:
    def __init__(self, data_file: str = "sujets0/competences_data.json"):
        self.data_file = Path(data_file)
        self.data = self._load_data()
    
    def _load_data(self) -> Dict:
        if self.data_file.exists():
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return self._create_default_structure()
    
    def get_competences_for_generator(self, generator_name: str) -> List[str]:
        return self.data.get("generators_mapping", {}).get(generator_name, {}).get("competences", [])
    
    def get_generators_for_competence(self, competence_id: str) -> List[str]:
        generators = []
        for gen_name, gen_data in self.data.get("generators_mapping", {}).items():
            if competence_id in gen_data.get("competences", []):
                generators.append(gen_name)
        return generators
    
    def get_statistics(self) -> Dict:
        return self.data.get("statistics", {})
```

### Phase 2 : Intégration avec le router

```python
# Dans src/sujets0/router.py
from .competences_manager import CompetencesManager

# Global instance
competences_manager = CompetencesManager()

@sujets0_router.get("/competences/{generator_name}")
async def get_generator_competences(generator_name: str):
    competences = competences_manager.get_competences_for_generator(generator_name)
    return {"generator": generator_name, "competences": competences}

@sujets0_router.get("/competences/stats")
async def get_competences_statistics():
    return competences_manager.get_statistics()
```

### Phase 3 : Interface d'administration

```python
# sujets0/admin_competences.py
def update_generator_competences(generator_name: str, competences: List[str]):
    """Mettre à jour les compétences d'un générateur"""
    pass

def validate_competences_data():
    """Valider la cohérence des données"""
    pass

def generate_statistics():
    """Recalculer les statistiques"""
    pass
```

## Services Proposés

### 1. Service de Requête
- Compétences par générateur
- Générateurs par compétence  
- Statistiques de répartition
- Recherche par domaine/difficulté

### 2. Service de Validation
- Vérification de l'existence des compétences
- Contrôle de cohérence des mappings
- Détection des générateurs non mappés

### 3. Service d'Analytics
- Fréquence d'utilisation des compétences
- Couverture des domaines
- Suggestions d'amélioration

## Intégration avec l'Interface

### Template Enhancement
```html
<!-- Dans les templates -->
<div class="competences-info">
    <h4>Compétences évaluées :</h4>
    <ul>
        {% for competence in question_competences %}
        <li class="badge badge-primary">{{ competence }}</li>
        {% endfor %}
    </ul>
</div>
```

### API Endpoints
- `GET /sujets0/competences/{generator}` : Compétences d'un générateur
- `GET /sujets0/competences/search?domain=fonctions` : Recherche par domaine
- `GET /sujets0/competences/stats` : Statistiques globales
- `POST /sujets0/competences/update` : Mise à jour (admin)

## Migration et Maintenance

### Scripts de Migration
```python
# scripts/migrate_competences.py
def migrate_from_markdown_to_json():
    """Migrer depuis le fichier markdown vers JSON"""
    pass

def backup_competences_data():
    """Sauvegarder les données"""
    pass
```

### Tests Automatisés
```python
# tests/test_competences.py
def test_all_generators_have_competences():
    """Vérifier que tous les générateurs ont des compétences assignées"""
    pass

def test_competences_exist():
    """Vérifier que toutes les compétences référencées existent"""
    pass
```

---

**Prochaines étapes recommandées** :
1. Créer le fichier JSON initial avec les données du markdown
2. Implémenter la classe `CompetencesManager`
3. Intégrer dans le router existant
4. Ajouter les endpoints d'API
5. Enrichir les templates avec les informations de compétences
