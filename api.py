from flask import Flask, request, jsonify
from flask_cors import CORS
from main import AnnuaireManager

app = Flask(__name__)
CORS(app)  # Permet les requêtes cross-origin depuis Node.js

# Gestionnaire d'annuaire
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
        contact = annuaire.obtenir_contact_par_id(contact_id)
        if not contact:
            return jsonify({"erreur": "Contact non trouvé"}), 404
        
        data = request.get_json()
        contact_modifie = annuaire.modifier_contact(contact_id, **data)
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
    return jsonify({"status": "ok"}), 200

# ============ GESTION DES ERREURS ============

@app.errorhandler(404)
def not_found(error):
    return jsonify({"erreur": "Ressource non trouvée"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"erreur": "Erreur serveur interne"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
