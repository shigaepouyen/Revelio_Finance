# Revelio Finance ✨

**Revelio Finance** est une application web de finances personnelles conçue pour apporter de la clarté à vos dépenses grâce à une analyse locale, privée et intelligente.

Le nom est un clin d'œil au sortilège de Révélation (*Revelio*) de l'univers Harry Potter. L'objectif de l'application est de "révéler" ce qui se cache dans vos relevés bancaires.

## 🎯 Le Concept

- **Confidentialité d'abord** : L'application fonctionne entièrement en local. Vous importez vos transactions via des fichiers OFX. Aucune donnée financière ne quitte votre machine.
- **Analyse Intelligente** : L'application intègre une intelligence artificielle (LLM) locale pour offrir une catégorisation sémantique, extrayant le marchand, la catégorie et la ville de chaque transaction.

## ⚙️ Statut Actuel (Phase 2 : L'Intelligence)

Le projet a atteint sa deuxième phase. Il permet de :

- **Importer** un fichier de transactions au format OFX via une interface web.
- **Analyser** le fichier pour en extraire les transactions.
- **Enrichir** chaque transaction en utilisant un LLM local (via Ollama) pour identifier le marchand, la catégorie, et la ville.
- **Afficher** les résultats dans un tableau clair et lisible.

## 📂 Structure du Projet

```
revelio-finance/
├── README.md
├── requirements.txt
├── backend/
│   ├── main.py             # Le serveur API FastAPI
│   ├── ai_service.py       # Le service d'interaction avec Ollama
│   ├── ofx_parser.py       # Le parser pour les fichiers OFX
│   ├── routers/            # Les routeurs de l'API
│   └── tests/              # Les tests unitaires
└── frontend/
    └── index.html          # L'interface utilisateur web
```

## 🚀 Démarrage Rapide

Pour faire fonctionner l'application, vous devez lancer deux services : le **serveur d'IA (Ollama)** et le **serveur de l'application (FastAPI)**.

### 1. Prérequis

- Python 3.8+
- [Ollama](https://ollama.com) installé sur votre machine.

### 2. Démarrage du Serveur d'IA

1.  **Téléchargez le modèle LLM :** Ouvrez un terminal et exécutez la commande suivante.
    ```bash
    ollama pull llama3.2:3b
    ```

2.  **Assurez-vous qu'Ollama est en cours d'exécution.** L'application Ollama doit tourner en arrière-plan pour que le backend puisse s'y connecter.

### 3. Démarrage du Serveur de l'Application

1.  **Clonez le projet** (si ce n'est pas déjà fait) et naviguez dans le dossier.

2.  **Créez un environnement virtuel** (recommandé) :
    ```bash
    python -m venv venv
    source venv/bin/activate  # Sur macOS/Linux
    .\venv\Scripts\activate   # Sur Windows
    ```

3.  **Installez les dépendances** Python :
    ```bash
    pip install -r requirements.txt
    ```

4.  **Lancez le serveur FastAPI :** Depuis la racine du projet, exécutez :
    ```bash
    uvicorn backend.main:app --reload
    ```

### 4. Utilisation

1.  Une fois le serveur démarré, ouvrez votre navigateur web et allez à l'adresse :
    `http://localhost:8000`

2.  Utilisez l'interface pour sélectionner votre fichier `.ofx` ou `.qfx` et cliquez sur "Analyser".

3.  Les transactions, enrichies par l'IA, apparaîtront dans un tableau sur la page.

## 🛠️ Stack Technique

- **Backend** : Python, FastAPI, Uvicorn
- **Analyse de données** : ofxtools
- **Intelligence Artificielle** : Ollama
- **Frontend** : HTML, JavaScript (utilisant l'API Fetch)
- **Tests** : Pytest, pytest-asyncio, Respx