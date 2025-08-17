# DRAFT DRAFT DRAFT 


> Proposition de Stockage des Données de Compétences

## Vue d'ensemble

Cette proposition détaille les différentes options pour stocker et utiliser les données de mapping entre générateurs et compétences.

## Options de Stockage

### 1. **Fichier JSON de Configuration** ⭐ **RECOMMANDÉ**

**Emplacement** : `src/sujets0/data/competences_mapping.json`

```json
{
  "metadata": {
    "version": "1.0",
    "last_updated": "2024-01-17",
    "description": "Mapping des générateurs Sujets 0 vers compétences BAC 1ère",
    "total_generators": 24,
    "total_competences": 41
  },
  "mapping": {
    "spe_sujet1_auto_01_question.py": {
      "competences": ["bac_1_auto_2_2DE", "bac_1_auto_4_2DE", "bac_1_auto_8_2DE"],
      "description": "Calculer l'inverse d'un multiple d'un nombre",
      "domaine": "calcul_numerique",
      "difficulte": "facile"
    },
    "spe_sujet1_auto_02_question.py": {
      "competences": ["bac_1_auto_2_2DE", "bac_1_auto_8_2DE", "bac_1_auto_12_2DE"],
      "description": "Évaluer F = a + b/(c*d) avec fractions",
      "domaine": "calcul_numerique",
      "difficulte": "moyen"
    }
  },
  "competences_index": {
    "bac_1_auto_1_2DE": {
      "titre": "Comparer des nombres réels",
      "domaine": "nombres",
      "generators": ["spe_sujet1_auto_09_question.py"]
    },
    "bac_1_auto_2_2DE": {
      "titre": "Opérations sur fractions",
      "domaine": "nombres", 
      "generators": ["spe_sujet1_auto_01_question.py", "spe_sujet1_auto_02_question.py"]
    }
  }
}
```

**Avantages** :
- ✅ Structure riche avec métadonnées
- ✅ Index inversé (compétence → générateurs)
- ✅ Facilement extensible
- ✅ Parsable par Python/JavaScript
- ✅ Validation possible avec JSON Schema

### 2. **Base de Données SQLite**

**Emplacement** : `src/sujets0/data/competences.db`

```sql
-- Table des générateurs
CREATE TABLE generators (
    id INTEGER PRIMARY KEY,
    filename VARCHAR(100) UNIQUE,
    description TEXT,
    domaine VARCHAR(50),
    difficulte VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table des compétences
CREATE TABLE competences (
    id VARCHAR(20) PRIMARY KEY,
    titre VARCHAR(200),
    domaine VARCHAR(50),
    description TEXT
);

-- Table de liaison (many-to-many)
CREATE TABLE generator_competences (
    generator_id INTEGER,
    competence_id VARCHAR(20),
    PRIMARY KEY (generator_id, competence_id),
    FOREIGN KEY (generator_id) REFERENCES generators(id),
    FOREIGN KEY (competence_id) REFERENCES competences(id)
);
```

**Avantages** :
- ✅ Requêtes SQL complexes
- ✅ Relations normalisées
- ✅ Performance pour gros volumes
- ❌ Plus complexe à maintenir

### 3. **Fichiers YAML Séparés**

**Structure** :
```
src/sujets0/data/
├── competences/
│   ├── spe_sujet1.yml
│   ├── spe_sujet2.yml
│   └── competences_ref.yml
└── schemas/
    └── competence_schema.yml
```

**Exemple** : `src/sujets0/data/competences/spe_sujet1.yml`
```yaml
generators:
  spe_sujet1_auto_01_question:
    competences:
      - bac_1_auto_2_2DE
      - bac_1_auto_4_2DE
      - bac_1_auto_8_2DE
    description: "Calculer l'inverse d'un multiple"
    domaine: calcul_numerique
    difficulte: facile
```

**Avantages** :
- ✅ Lisible et éditable
- ✅ Structure par sujet
- ✅ Validation avec schémas
- ❌ Fragmentation des données

### 4. **Configuration Python**

**Emplacement** : `src/sujets0/config/competences.py`

```python
from typing import Dict, List, NamedTuple

class GeneratorCompetence(NamedTuple):
    competences: List[str]
    description: str
    domaine: str
    difficulte: str

COMPETENCES_MAPPING: Dict[str, GeneratorCompetence] = {
    "spe_sujet1_auto_01_question.py": GeneratorCompetence(
        competences=["bac_1_auto_2_2DE", "bac_1_auto_4_2DE", "bac_1_auto_8_2DE"],
        description="Calculer l'inverse d'un multiple d'un nombre",
        domaine="calcul_numerique",
        difficulte="facile"
    ),
    # ...
}

# Index inversé
COMPETENCE_TO_GENERATORS: Dict[str, List[str]] = {
    "bac_1_auto_2_2DE": ["spe_sujet1_auto_01_question.py", "spe_sujet1_auto_02_question.py"],
    # ...
}
```

**Avantages** :
- ✅ Type safety avec Python
- ✅ Import direct dans le code
- ✅ Validation à l'exécution
- ❌ Moins flexible pour édition

## Recommandation : Option JSON

### Structure Recommandée

```
src/sujets0/
├── data/
│   ├── competences_mapping.json     # Données principales
│   ├── competences_schema.json      # Validation JSON Schema
│   └── README.md                    # Documentation des données
├── services/
│   ├── __init__.py
│   ├── competences_service.py       # Service d'accès aux données
│   └── competences_analyzer.py      # Analyses et statistiques
├── scripts/
│   ├── validate_mapping.py          # Validation des données
│   ├── generate_stats.py            # Génération de statistiques
│   └── export_mapping.py            # Export vers autres formats
└── COMPETENCES_MAPPING.md           # Documentation complète
```

### Service d'Accès

```python
# src/sujets0/services/competences_service.py
import json
from pathlib import Path
from typing import Dict, List, Optional

class CompetencesService:
    def __init__(self):
        self.data_path = Path(__file__).parent.parent / "data" / "competences_mapping.json"
        self._data = None
    
    def load_data(self) -> Dict:
        if self._data is None:
            with open(self.data_path, 'r', encoding='utf-8') as f:
                self._data = json.load(f)
        return self._data
    
    def get_competences_for_generator(self, filename: str) -> List[str]:
        data = self.load_data()
        return data["mapping"].get(filename, {}).get("competences", [])
    
    def get_generators_for_competence(self, competence_id: str) -> List[str]:
        data = self.load_data()
        return data["competences_index"].get(competence_id, {}).get("generators", [])
    
    def get_statistics(self) -> Dict:
        # Génération de statistiques automatiques
        pass
```

### Intégration dans le Router

```python
# src/sujets0/router.py
from .services.competences_service import CompetencesService

competences_service = CompetencesService()

@sujets0_router.get("/sujets0-competences/{generator_name}")
async def get_generator_competences(generator_name: str):
    competences = competences_service.get_competences_for_generator(generator_name)
    return {"generator": generator_name, "competences": competences}
```

## Prochaines Étapes

1. **Créer la structure JSON** avec les données fournies
2. **Développer le service d'accès** pour l'intégration
3. **Ajouter les métadonnées** (domaines, difficultés)
4. **Créer les scripts de validation** et maintenance
5. **Intégrer dans l'interface QCM** pour afficher les compétences testées

Cette approche offre le meilleur équilibre entre flexibilité, performance et maintenabilité.
