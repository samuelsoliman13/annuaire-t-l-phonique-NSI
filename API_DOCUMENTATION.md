# Documentation de l'API Annuaire

## Installation

```bash
pip install -r requirements.txt
```

## Démarrage du serveur

```bash
python api.py
```

L'API sera disponible sur `http://localhost:5001`

---

## Endpoints disponibles

### 1. Récupérer tous les contacts
**GET** `/api/contacts`

**Réponse (200):**
```json
[
  {
    "id": 1,
    "nom": "Dupont",
    "prenom": "Jean",
    "email": "jean@example.com",
    "telephone": "06 12 34 56 78",
    "adresse": "123 rue de Paris",
    "adresse_travail": "456 av de l'Industrie",
    "date_creation": "2026-01-23T10:30:00"
  }
]
```

---

### 2. Récupérer un contact spécifique
**GET** `/api/contacts/<id>`

**Exemple:** `GET /api/contacts/1`

**Réponse (200):**
```json
{
  "id": 1,
  "nom": "Dupont",
  "prenom": "Jean",
  ...
}
```

**Erreur (404):** Contact non trouvé

---

### 3. Créer un nouveau contact
**POST** `/api/contacts`

**Body (JSON):**
```json
{
  "nom": "Martin",
  "prenom": "Sophie",
  "email": "sophie.martin@example.com",
  "telephone": "07 98 76 54 32",
  "adresse": "789 boulevard Saint-Germain, 75005 Paris",
  "adresse_travail": "200 rue de Rivoli, 75001 Paris"
}
```

**Réponse (201):**
```json
{
  "id": 2,
  "nom": "Martin",
  "prenom": "Sophie",
  "email": "sophie.martin@example.com",
  "telephone": "07 98 76 54 32",
  "adresse": "789 boulevard Saint-Germain, 75005 Paris",
  "adresse_travail": "200 rue de Rivoli, 75001 Paris",
  "date_creation": "2026-01-23T10:35:00"
}
```

**Erreur (400):** Champ manquant

---

### 4. Modifier un contact
**PUT** `/api/contacts/<id>`

**Body (JSON) - Champs optionnels:**
```json
{
  "nom": "Dupont-Martin",
  "email": "nouveau@example.com",
  "telephone": "06 11 22 33 44"
}
```

**Réponse (200):**
```json
{
  "id": 1,
  "nom": "Dupont-Martin",
  ...
  "date_modification": "2026-01-23T11:00:00"
}
```

---

### 5. Supprimer un contact
**DELETE** `/api/contacts/<id>`

**Réponse (200):**
```json
{
  "message": "Contact supprimé avec succès"
}
```

**Erreur (404):** Contact non trouvé

---

### 6. Rechercher des contacts
**GET** `/api/contacts/search?q=<terme>`

**Exemple:** `GET /api/contacts/search?q=Dupont`

**Réponse (200):**
```json
[
  {
    "id": 1,
    "nom": "Dupont",
    ...
  }
]
```

La recherche se fait sur les champs: **nom**, **prénom**, et **email** (insensible à la casse)

---

### 7. Statistiques
**GET** `/api/stats`

**Réponse (200):**
```json
{
  "total_contacts": 5,
  "date_consultation": "2026-01-23T11:15:00"
}
```

---

### 8. Vérifier l'état du serveur
**GET** `/api/health`

**Réponse (200):**
```json
{
  "status": "ok"
}
```

---

## Codes de réponse HTTP

- **200** : Succès (GET, PUT, DELETE)
- **201** : Créé avec succès (POST)
- **400** : Requête invalide (données manquantes ou mal formées)
- **404** : Ressource non trouvée
- **500** : Erreur serveur interne

---

## Exemples avec curl

```bash
# Récupérer tous les contacts
curl http://localhost:5000/api/contacts

# Créer un contact
curl -X POST http://localhost:5000/api/contacts \
  -H "Content-Type: application/json" \
  -d '{
    "nom": "Dupont",
    "prenom": "Jean",
    "email": "jean@example.com",
    "telephone": "06 12 34 56 78",
    "adresse": "123 rue de Paris",
    "adresse_travail": "456 av Industrie"
  }'

# Modifier un contact
curl -X PUT http://localhost:5000/api/contacts/1 \
  -H "Content-Type: application/json" \
  -d '{"telephone": "06 99 88 77 66"}'

# Supprimer un contact
curl -X DELETE http://localhost:5000/api/contacts/1

# Rechercher des contacts
curl "http://localhost:5000/api/contacts/search?q=Dupont"
```

---

## Exemples avec Node.js/Fetch

```javascript
// Récupérer tous les contacts
fetch('http://localhost:5000/api/contacts')
  .then(res => res.json())
  .then(data => console.log(data));

// Créer un contact
fetch('http://localhost:5000/api/contacts', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    nom: 'Dupont',
    prenom: 'Jean',
    email: 'jean@example.com',
    telephone: '06 12 34 56 78',
    adresse: '123 rue de Paris',
    adresse_travail: '456 av Industrie'
  })
})
.then(res => res.json())
.then(data => console.log(data));

// Modifier un contact
fetch('http://localhost:5000/api/contacts/1', {
  method: 'PUT',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ telephone: '06 99 88 77 66' })
})
.then(res => res.json())
.then(data => console.log(data));

// Supprimer un contact
fetch('http://localhost:5000/api/contacts/1', { method: 'DELETE' })
.then(res => res.json())
.then(data => console.log(data));

// Rechercher
fetch('http://localhost:5000/api/contacts/search?q=Dupont')
  .then(res => res.json())
  .then(data => console.log(data));
```
