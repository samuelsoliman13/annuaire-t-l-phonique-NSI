from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from typing import List, Dict, Optional
import os

app = Flask(__name__)
CORS(app)

# Initialiser SQLAlchemy
db = SQLAlchemy()

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

class AnnuaireManager:
    """Gestionnaire de l'annuaire téléphonique."""
    
    def __init__(self, db_uri: str):
        app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db.init_app(app)
        with app.app_context():
            db.create_all()
    
    def ajouter_contact(self, nom: str, prenom: str, email: str, 
                       telephone: str, adresse: str, adresse_travail: str) -> Dict:
        """Ajoute un nouveau contact à l'annuaire."""
        contact = Contact(
            nom=nom.strip(),
            prenom=prenom.strip(),
            email=email.strip(),
            telephone=telephone.strip(),
            adresse=adresse.strip(),
            adresse_travail=adresse_travail.strip()
        )
        with app.app_context():
            db.session.add(contact)
            db.session.commit()
            return contact.to_dict()
    
    def obtenir_tous_les_contacts(self) -> List[Dict]:
        """Retourne tous les contacts."""
        with app.app_context():
            return [contact.to_dict() for contact in Contact.query.all()]
    
    def obtenir_contact_par_id(self, contact_id: int) -> Optional[Dict]:
        """Retourne un contact par son ID."""
        with app.app_context():
            contact = Contact.query.get(contact_id)
            return contact.to_dict() if contact else None
    
    def rechercher_contacts(self, terme: str) -> List[Dict]:
        """Recherche les contacts par nom, prénom ou email."""
        terme_lower = terme.lower()
        with app.app_context():
            resultats = Contact.query.filter(
                (Contact.nom.ilike(f'%{terme_lower}%')) |
                (Contact.prenom.ilike(f'%{terme_lower}%')) |
                (Contact.email.ilike(f'%{terme_lower}%'))
            ).all()
            return [contact.to_dict() for contact in resultats]
    
    def modifier_contact(self, contact_id: int, **kwargs) -> Optional[Dict]:
        """Modifie un contact existant."""
        with app.app_context():
            contact = Contact.query.get(contact_id)
            if not contact:
                return None
            
            champs_autoises = ['nom', 'prenom', 'email', 'telephone', 'adresse', 'adresse_travail']
            for key, value in kwargs.items():
                if key in champs_autoises and value is not None:
                    setattr(contact, key, str(value).strip())
            
            db.session.commit()
            return contact.to_dict()
    
    def supprimer_contact(self, contact_id: int) -> bool:
        """Supprime un contact de l'annuaire."""
        with app.app_context():
            contact = Contact.query.get(contact_id)
            if contact:
                db.session.delete(contact)
                db.session.commit()
                return True
            return False
    
    def obtenir_stats(self) -> Dict:
        """Retourne des statistiques sur l'annuaire."""
        with app.app_context():
            return {
                "total_contacts": Contact.query.count(),
                "date_consultation": datetime.now().isoformat()
            }

# Instance du gestionnaire global (sera initialisée avec DB_URI)
annuaire = None


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
                # request.get_json() de Flask peut renvoyer None si Content-Type n'est pas application/json        data = request.get_json() or {} 
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

@app.route('/api/init-db', methods=['POST'])
def init_db():
    """Initialise la base de données. Utilisé pour configurer l'URI de la DB."""
    data = request.get_json()
    db_uri = data.get('db_uri')
    if not db_uri:
        return jsonify({"erreur": "db_uri manquant"}), 400
    
    global annuaire
    annuaire = AnnuaireManager(db_uri)
    return jsonify({"message": "Base de données initialisée avec succès"}), 200

# ============ ROUTES UTILITAIRES ============

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Récupère les statistiques de l'annuaire."""
    return jsonify(annuaire.obtenir_stats()), 200

@app.route('/api/health', methods=['GET'])
def health_check():
    """Vérifie l'état de l'API."""
    return jsonify({"status": "ok"}), 200

# ============ GESTION DES ERREURS ============

@app.errorhandler(404)
def not_found(error):
    return jsonify({"erreur": "Ressource non trouvée"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"erreur": "Erreur serveur interne"}), 500

if __name__ == '__main__':
    # Par défaut, utiliser une base de données SQLite locale si non initialisée via /api/init-db
    if annuaire is None:
        db_path = os.path.join(os.getcwd(), 'contacts.db')
        annuaire = AnnuaireManager(f'sqlite:///{db_path}')
    app.run(debug=True, host='0.0.0.0', port=5000)