# Revelio Finance ✨

**Revelio Finance** est une application web de finances personnelles conçue pour apporter de la clarté à vos dépenses grâce à une analyse locale, privée et intelligente.

Le nom est un clin d'œil au sortilège de Révélation (*Revelio*) de l'univers Harry Potter. L'objectif de l'application est de "révéler" ce qui se cache dans vos relevés bancaires : les abonnements oubliés, les schémas de dépenses et les anomalies.

## 🎯 Le Concept

Contrairement à la plupart des applications de gestion de budget, **Revelio Finance** est construit sur un principe fondamental : la souveraineté de vos données.

- **Confidentialité d'abord** : L'application fonctionne entièrement en local. Vous importez vos transactions via des fichiers OFX exportés depuis votre banque. Aucun identifiant bancaire n'est partagé, aucune donnée financière ne quitte votre machine.  
- **Analyse Intelligente** : L'objectif à terme est d'intégrer une intelligence artificielle (LLM) locale pour offrir une catégorisation sémantique, une détection des dépenses récurrentes et une identification d'anomalies bien plus puissantes que les systèmes basés sur des règles simples.  
- **Interface Claire** : Le but est de présenter vos finances de manière simple et visuelle, pour vous aider à prendre de meilleures décisions sans vous noyer dans des tableaux de chiffres complexes.

## ⚙️ Statut Actuel (Phase 1 : Le Socle Fonctionnel)

Le projet est actuellement dans sa première phase. Le socle fonctionnel est en place et permet de :

- Importer un fichier de transactions au format OFX  
- Analyser (parser) le fichier pour en extraire les informations clés (date, description, montant)  
- Afficher les transactions dans une interface web claire  
- Appliquer une catégorisation automatique de base via un système de règles simples  
- Permettre la catégorisation manuelle pour chaque transaction (dans le prototype)

## 📂 Structure du Projet

```
finance_app/
├── README.md               # Ce fichier
├── ofx_parser.py           # Le script principal pour analyser les fichiers OFX
├── requirements.txt        # Les dépendances Python du projet
├── prototype/
│   └── prototype_app.py    # L'application de prototypage rapide avec Streamlit
├── backend/
│   ├── ofx_parser.py       # Une copie du parser pour le backend
│   └── main.py             # Le serveur API avec FastAPI
└── frontend/
    └── index.html          # La page web simple pour l'interface utilisateur
```

## 🚀 Démarrage Rapide

### 1. Prérequis

- Python 3.8+  
- `pip` (le gestionnaire de paquets Python)

### 2. Installation

1. **Clonez le projet** (ou téléchargez et décompressez l'archive) :
    ```bash
    git clone <url-du-repository>
    cd finance_app
    ```

2. **Créez un environnement virtuel** (recommandé) :
    ```bash
    python -m venv venv
    source venv/bin/activate  # Sur macOS/Linux
    .\venv\Scripts\activate   # Sur Windows
    ```

3. **Installez les dépendances** :
    ```bash
    pip install -r requirements.txt
    ```

#### Exemple de contenu du `requirements.txt` :
```
ofxtools
streamlit
pandas
fastapi
uvicorn[standard]
python-multipart
```

### 3. Utilisation

Vous pouvez lancer deux versions de l'application : le **prototype rapide** ou l'**architecture de production** (backend + frontend).

#### Option A : Lancer le Prototype Streamlit

1. Assurez-vous d'avoir une copie de `ofx_parser.py` dans le dossier `prototype/`.  
2. Lancez la commande :
    ```bash
    streamlit run prototype/prototype_app.py
    ```
3. Ouvrez votre navigateur à l'adresse indiquée (souvent `http://localhost:8501`).

#### Option B : Lancer l'Application Complète (V1)

1. **Lancez le serveur backend (API)** :
    ```bash
    uvicorn backend.main:app --reload
    ```
    Le serveur sera accessible à `http://localhost:8000`.

2. **Ouvrez l'interface frontend** :
    - Naviguez jusqu'au dossier `frontend/`  
    - Ouvrez `index.html` dans votre navigateur

## 🛠️ Stack Technique

- **Backend** : Python, FastAPI, Uvicorn  
- **Analyse de données** : ofxtools, Pandas  
- **Prototypage** : Streamlit  
- **Frontend (V1)** : HTML, CSS, JavaScript

## 🗺️ Feuille de Route

### Phase 2 : L'Intelligence
- [ ] Intégrer un LLM local (via Ollama) pour la catégorisation sémantique  
- [ ] Développer un module de détection d'anomalies basé sur l'IA  
- [ ] Mettre en place une base de données (SQLite puis PostgreSQL)

### Phase 3 : L'Expérience
- [ ] Refondre le frontend avec un framework moderne (React ou Vue.js)  
- [ ] Ajouter des visualisations de données avancées  
- [ ] Développer des fonctionnalités de conseil et d'aperçus financiers générés par l'IA
