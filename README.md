# 📒 Annuaire Téléphonique

Une application desktop multiplateforme de gestion de contacts, construite avec **Electron**, **Node.js** et un backend **Python Flask**. L'application offre une flexibilité totale sur le stockage des données : base de données locale SQLite ou API distante.

> Projet NSI — Samuel Soliman & Théo De la Chapelle

---

## Fonctionnalités

- **Ajouter** un contact (nom, prénom, email, téléphone, adresse, adresse de travail)
- **Modifier** un contact existant
- **Supprimer** un contact (avec confirmation)
- **Rechercher** un contact par nom, prénom ou email
- **Choix du stockage** : base locale SQLite ou API distante
- **Mémorisation** du choix de connexion au lancement
- **Validation** des champs (format email, exactement 10 chiffres pour le téléphone)

---

## Architecture

```
┌─────────────────────────────────────────────┐
│              Electron (Frontend)             │
│                                             │
│  ┌─────────────┐      ┌──────────────────┐  │
│  │ choiceWindow│      │   mainWindow     │  │
│  │ (choice.js) │      │   (index.js)     │  │
│  └──────┬──────┘      └────────┬─────────┘  │
│         │    preload.js (IPC)  │             │
│         └──────────┬───────────┘             │
│                    │                         │
│             main.js (Main Process)           │
└────────────────────┬────────────────────────┘
                     │ HTTP REST
          ┌──────────┴──────────┐
          │                     │
   ┌──────┴──────┐     ┌────────┴───────┐
   │ Flask local │     │  API distante  │
   │ (api_server)│     │  (URL custom   │
   │  SQLite DB  │     │   ou Théo)     │
   └─────────────┘     └────────────────┘
```

**Composants principaux :**

- `main.js` — Processus principal Electron, gestion des fenêtres, spawn du serveur Python
- `preload.js` — Pont sécurisé entre le renderer et le main process (contextBridge)
- `choice.js` — Interface de sélection de la base de données
- `index.js` — Interface principale de gestion des contacts
- `api_server.py` — API REST Flask avec SQLAlchemy

---

## Installation & Lancement

### Prérequis

- [Node.js](https://nodejs.org/) >= 12
- [Python](https://www.python.org/) >= 3.8

### Installation

```bash
# Cloner le dépôt
git clone https://github.com/samuelsoliman13/annuaire-t-l-phonique-NSI.git
cd annuaire-t-l-phonique-NSI

# Installer les dépendances Node.js
npm install

# Installer les dépendances Python
pip install -r requirements.txt
```

### Lancement

```bash
npm start
```

Au lancement, une fenêtre vous propose trois options :

| Option | Description |
|--------|-------------|
| **Local Database** | Lance automatiquement le serveur Flask en arrière-plan avec SQLite |
| **Théo's Server** | Se connecte à `https://annuaire.dlchost.com` (vérifie la disponibilité) |
| **Remote Database** | Saisir l'URL d'une API distante compatible |

>  Cochez **"Remember my choice"** pour ne plus voir cette fenêtre au prochain lancement.

---

## 🔧 API REST

Le serveur Flask tourne sur `http://localhost:5001` en mode local.

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| `GET` | `/api/contacts` | Récupérer tous les contacts |
| `GET` | `/api/contacts/<id>` | Récupérer un contact par ID |
| `POST` | `/api/contacts` | Créer un nouveau contact |
| `PUT` | `/api/contacts/<id>` | Modifier un contact |
| `DELETE` | `/api/contacts/<id>` | Supprimer un contact |
| `GET` | `/api/contacts/search?q=` | Rechercher (nom, prénom, email) |
| `GET` | `/api/stats` | Statistiques de l'annuaire |
| `GET` | `/api/health` | État du serveur |

### Exemple — Créer un contact

```bash
curl -X POST http://localhost:5001/api/contacts \
  -H "Content-Type: application/json" \
  -d '{
    "nom": "Dupont",
    "prenom": "Jean",
    "email": "jean@example.com",
    "telephone": "0612345678",
    "adresse": "123 rue de Paris",
    "adresse_travail": "456 av de l Industrie"
  }'
```

> Pour la documentation complète de l'API, voir [API_DOCUMENTATION.md](./API_DOCUMENTATION.md)

---

## Build — Générer l'exécutable

```bash
# Build du binaire Python (PyInstaller)
npm run build:python

# Build de l'application Electron
npm run dist
```

L'installateur Windows (`.exe`) sera généré dans le dossier `dist/`.

> Le binaire Python est embarqué dans les ressources de l'application via `extraResources` dans `package.json`.

---

## 🗂️ Structure du projet

```
annuaire-téléphonique/
├── main.js              # Processus principal Electron
├── preload.js           # Bridge sécurisé IPC / contextBridge
├── index.html           # Interface principale
├── index.js             # Logique renderer — gestion contacts
├── choice.html          # Interface de choix de BDD
├── choice.js            # Logique renderer — choix connexion
├── style.css            # Styles interface principale
├── choice.css           # Styles interface de choix
├── api_server.py        # Backend Flask + SQLAlchemy
├── api_server.spec      # Configuration PyInstaller
├── requirements.txt     # Dépendances Python
├── package.json         # Dépendances Node.js + config build
└── API_DOCUMENTATION.md # Documentation complète de l'API
```

---
## Diagramme d'usage
'''
![Description](./assets/screenshot.png)
'''
---
## 🛠️ Stack technique

| Couche | Technologie |
|--------|-------------|
| Desktop | Electron 40 |
| Frontend | HTML5, CSS3, JavaScript Vanilla |
| Backend | Python 3, Flask, Flask-SQLAlchemy |
| Base de données | SQLite (local) |
| Persistance préférences | electron-store |
| Communication | IPC Electron + REST HTTP |
| Build | electron-builder, PyInstaller |

---

## 👥 Auteurs

- **Samuel Soliman** — Backend Python, base de données
- **Théo De la Chapelle** — Application Electron, frontend, hébergement serveur distant

---

## 📄 Licence

ISC
