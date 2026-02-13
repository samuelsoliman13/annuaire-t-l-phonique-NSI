from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import os
import argparse
import re

parser = argparse.ArgumentParser(description="Run the Flask for Annuaire Téléphonique.")
parser.add_argument('--db-uri', type=str, default=None,
help='The database URI for SQLAlchemy.')
args = parser.parse_args()

app = Flask(__name__)

# Configuration CORS pour accepter les requêtes depuis n'importe quel domaine
CORS(app, resources={
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Fonctions de validation
def validate_email(email: str) -> Tuple[bool, str]:
    """Valide le format de l'email."""
    email = email.strip()
    if not email:
        return False, "L'email ne peut pas être vide"
    
    if '@' not in email:
        return False, "L'email doit contenir un @"
    if '.' not in email:
        return False, "L'email doit contenir un ."

    # Regex basique pour valider le format email
    email_regex = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
    if not re.match(email_regex, email):
        return False, "Format d'email invalide"
    
    return True, ""

def validate_telephone(telephone: str) -> Tuple[bool, str]:
    """Valide le format du téléphone (exactement 10 chiffres)."""
    telephone = telephone.strip()
    if not telephone:
        return False, "Le téléphone ne peut pas être vide"
    
    # Extraire seulement les chiffres
    digits_only = re.sub(r'\D', '', telephone)
    
    if len(digits_only) != 10:
        return False, "Le téléphone doit contenir exactement 10 chiffres"
    
    return True, ""

# Initialiser SQLAlchemy
db = SQLAlchemy()

# Configuration de la base de données
# Priorité: argument CLI > variable d'environnement > SQLite local par défaut
if args.db_uri:
    database_uri = args.db_uri
elif os.getenv('DATABASE_URL'):
    database_uri = os.getenv('DATABASE_URL')
    # Heroku utilise postgres:// mais SQLAlchemy nécessite postgresql://
    if database_uri.startswith('postgres://'):
        database_uri = database_uri.replace('postgres://', 'postgresql://', 1)
else:
    database_uri = 'sqlite:///contacts.db'

app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
db.init_app(app)

print(f"Using database: {database_uri}")


# IMPORTANT: Define the Contact model BEFORE calling db.create_all()
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(80), nullable=False)
    prenom = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    telephone = db.Column(db.String(20), nullable=False)
    adresse = db.Column(db.String(200), nullable=False)
    adresse_travail = db.Column(db.String(200), nullable=False)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    date_modification = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "nom": self.nom,
            "prenom": self.prenom,
            "email": self.email,
            "telephone": self.telephone,
            "adresse": self.adresse,
            "adresse_travail": self.adresse_travail,
            "date_creation": self.date_creation.isoformat(),
            "date_modification": self.date_modification.isoformat() if self.date_modification else None,
        }


# Create tables after models are defined
with app.app_context():
    db.create_all()


class AnnuaireManager:
    """Gestionnaire de l'annuaire téléphonique."""
    
    def __init__(self):
        """Gestionnaire de l'annuaire téléphonique.
        Initialise sans prendre db_uri, car la configuration est globale."""
        pass
    
    def ajouter_contact(self, nom: str, prenom: str, email: str, telephone: str = "", adresse: str = "", adresse_travail: str = ""):
        """Ajoute un nouveau contact à l'annuaire."""
        contact = Contact(
            nom=nom.strip(),
            prenom=prenom.strip(),
            email=email.strip(),
            telephone=telephone.strip(),
            adresse=adresse.strip(),
            adresse_travail=adresse_travail.strip()
        )
        db.session.add(contact)
        db.session.commit()
        return contact.to_dict()
    
    def obtenir_tous_les_contacts(self) -> List[Dict]:
        """Retourne tous les contacts."""
        return [contact.to_dict() for contact in Contact.query.all()]
    
    def obtenir_contact_par_id(self, contact_id: int) -> Optional[Dict]:
        """Retourne un contact par son ID."""
        contact = db.session.get(Contact, contact_id)
        return contact.to_dict() if contact else None
    
    def rechercher_contacts(self, terme: str) -> List[Dict]:
        """Recherche les contacts par nom, prénom ou email."""
        terme_lower = terme.lower()
        resultats = Contact.query.filter(
            (Contact.nom.ilike(f'%{terme_lower}%')) |
            (Contact.prenom.ilike(f'%{terme_lower}%')) |
            (Contact.email.ilike(f'%{terme_lower}%'))
        ).all()
        return [contact.to_dict() for contact in resultats]
    
    def modifier_contact(self, contact_id: int, **kwargs) -> Optional[Dict]:
        """Modifie un contact existant."""
        contact = db.session.get(Contact, contact_id)
        if not contact:
            return None
        
        champs_autorises = ['nom', 'prenom', 'email', 'telephone', 'adresse', 'adresse_travail']
        for key, value in kwargs.items():
            if key in champs_autorises and value is not None:
                setattr(contact, key, str(value).strip())
        
        db.session.commit()
        return contact.to_dict()
    
    def supprimer_contact(self, contact_id: int) -> bool:
        """Supprime un contact de l'annuaire."""
        contact = db.session.get(Contact, contact_id)
        if contact:
            db.session.delete(contact)
            db.session.commit()
            return True
        return False
    
    def obtenir_stats(self) -> Dict:
        """Retourne des statistiques sur l'annuaire."""
        return {
            "total_contacts": Contact.query.count(),
            "date_consultation": datetime.now().isoformat()
        }


# Instance du gestionnaire global
annuaire = AnnuaireManager()


# ============ ROUTES POUR LES CONTACTS ============

@app.route('/api/contacts', methods=['GET'])
def get_all_contacts():
    """Récupère tous les contacts."""
    return jsonify(annuaire.obtenir_tous_les_contacts()), 200


@app.route('/api/contacts/<int:contact_id>', methods=['GET'])
def get_contact(contact_id):
    """Récupère un contact spécifique."""
    contact = annuaire.obtenir_contact_par_id(contact_id)
    if not contact:
        return jsonify({"erreur": "Contact non trouvé"}), 404
    return jsonify(contact), 200


@app.route('/api/contacts', methods=['POST'])
def create_contact():
    """Crée un nouveau contact."""
    try:
        data = request.get_json()
        
        # Validation des champs requis
        champs_requis = ['nom', 'prenom', 'email', 'telephone', 'adresse', 'adresse_travail']
        for champ in champs_requis:
            if champ not in data or not data[champ]:
                return jsonify({"erreur": f"Le champ '{champ}' est requis"}), 400
        
        # Valider l'email
        email_valid, email_error = validate_email(data['email'])
        if not email_valid:
            return jsonify({"erreur": email_error}), 400
        
        # Valider le téléphone
        phone_valid, phone_error = validate_telephone(data['telephone'])
        if not phone_valid:
            return jsonify({"erreur": phone_error}), 400
        
        contact = annuaire.ajouter_contact(
            nom=data['nom'],
            prenom=data['prenom'],
            email=data['email'],
            telephone=data['telephone'],
            adresse=data['adresse'],
            adresse_travail=data['adresse_travail']
        )
        return jsonify(contact), 201
    except Exception as e:
        return jsonify({"erreur": str(e)}), 400


@app.route('/api/contacts/<int:contact_id>', methods=['PUT'])
def update_contact(contact_id):
    """Modifie un contact existant."""
    try:
        # request.get_json() de Flask peut renvoyer None si Content-Type n'est pas application/json
        data = request.get_json() or {} 
        
        # Valider l'email s'il est fourni
        if 'email' in data and data['email']:
            email_valid, email_error = validate_email(data['email'])
            if not email_valid:
                return jsonify({"erreur": email_error}), 400
        
        # Valider le téléphone s'il est fourni
        if 'telephone' in data and data['telephone']:
            phone_valid, phone_error = validate_telephone(data['telephone'])
            if not phone_valid:
                return jsonify({"erreur": phone_error}), 400
        
        contact_modifie = annuaire.modifier_contact(contact_id, **data)
        if not contact_modifie:
            return jsonify({"erreur": "Contact non trouvé"}), 404
        return jsonify(contact_modifie), 200
    except Exception as e:
        return jsonify({"erreur": str(e)}), 400


@app.route('/api/contacts/<int:contact_id>', methods=['DELETE'])
def delete_contact(contact_id):
    """Supprime un contact."""
    if annuaire.supprimer_contact(contact_id):
        return jsonify({"message": "Contact supprimé avec succès"}), 200
    return jsonify({"erreur": "Contact non trouvé"}), 404


@app.route('/api/contacts/search', methods=['GET'])
def search_contacts():
    """Recherche les contacts par terme."""
    terme = request.args.get('q', '')
    if not terme:
        return jsonify({"erreur": "Paramètre 'q' manquant"}), 400
    
    resultats = annuaire.rechercher_contacts(terme)
    return jsonify(resultats), 200


# ============ ROUTES UTILITAIRES ============

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Récupère les statistiques de l'annuaire."""
    return jsonify(annuaire.obtenir_stats()), 200


@app.route('/api/health', methods=['GET'])
def health_check():
    """Vérifie l'état de l'API."""
    try:
        # Test de connexion à la base de données
        db.session.execute(db.text('SELECT 1'))
        return jsonify({
            "status": "ok",
            "database": "connected"
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "database": "disconnected",
            "error": str(e)
        }), 500


# ============ GESTION DES ERREURS ============

@app.errorhandler(404)
def not_found(error):
    return jsonify({"erreur": "Ressource non trouvée"}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({"erreur": "Erreur serveur interne"}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)