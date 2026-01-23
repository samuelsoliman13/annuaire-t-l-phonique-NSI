import json
import os
from datetime import datetime
from typing import List, Dict, Optional

# Configuration
DB_FILE = "contacts.json"

class AnnuaireManager:
    """Gestionnaire de l'annuaire téléphonique."""
    
    def __init__(self, db_file: str = DB_FILE):
        self.db_file = db_file
        self.contacts = self._load_database()
    
    def _load_database(self) -> List[Dict]:
        """Charge les contacts depuis la base de données JSON."""
        if not os.path.exists(self.db_file):
            return []
        try:
            with open(self.db_file, 'r', encoding='utf-8') as file:
                data = json.load(file)
                return data if isinstance(data, list) else []
        except (json.JSONDecodeError, IOError):
            return []
    
    def _save_database(self) -> None:
        """Sauvegarde les contacts dans la base de données JSON."""
        with open(self.db_file, 'w', encoding='utf-8') as file:
            json.dump(self.contacts, file, indent=4, ensure_ascii=False)
    
    def _get_next_id(self) -> int:
        """Génère le prochain ID disponible."""
        if not self.contacts:
            return 1
        return max(contact.get('id', 0) for contact in self.contacts) + 1
    
    def ajouter_contact(self, nom: str, prenom: str, email: str, 
                       telephone: str, adresse: str, adresse_travail: str) -> Dict:
        """Ajoute un nouveau contact à l'annuaire."""
        contact = {
            "id": self._get_next_id(),
            "nom": nom.strip(),
            "prenom": prenom.strip(),
            "email": email.strip(),
            "telephone": telephone.strip(),
            "adresse": adresse.strip(),
            "adresse_travail": adresse_travail.strip(),
            "date_creation": datetime.now().isoformat()
        }
        self.contacts.append(contact)
        self._save_database()
        return contact
    
    def obtenir_tous_les_contacts(self) -> List[Dict]:
        """Retourne tous les contacts."""
        return self.contacts
    
    def obtenir_contact_par_id(self, contact_id: int) -> Optional[Dict]:
        """Retourne un contact par son ID."""
        for contact in self.contacts:
            if contact.get('id') == contact_id:
                return contact
        return None
    
    def rechercher_contacts(self, terme: str) -> List[Dict]:
        """Recherche les contacts par nom, prénom ou email."""
        terme_lower = terme.lower()
        resultats = []
        for contact in self.contacts:
            if (terme_lower in contact['nom'].lower() or 
                terme_lower in contact['prenom'].lower() or 
                terme_lower in contact['email'].lower()):
                resultats.append(contact)
        return resultats
    
    def modifier_contact(self, contact_id: int, **kwargs) -> Optional[Dict]:
        """Modifie un contact existant."""
        contact = self.obtenir_contact_par_id(contact_id)
        if not contact:
            return None
        
        # Champs autorisés
        champs_autoises = ['nom', 'prenom', 'email', 'telephone', 'adresse', 'adresse_travail']
        for key, value in kwargs.items():
            if key in champs_autoises and value is not None:
                contact[key] = str(value).strip()
        
        contact['date_modification'] = datetime.now().isoformat()
        self._save_database()
        return contact
    
    def supprimer_contact(self, contact_id: int) -> bool:
        """Supprime un contact de l'annuaire."""
        for i, contact in enumerate(self.contacts):
            if contact.get('id') == contact_id:
                self.contacts.pop(i)
                self._save_database()
                return True
        return False
    
    def obtenir_stats(self) -> Dict:
        """Retourne des statistiques sur l'annuaire."""
        return {
            "total_contacts": len(self.contacts),
            "date_consultation": datetime.now().isoformat()
        }


# Instance globale du gestionnaire
annuaire = AnnuaireManager()


# Fonctions de compatibilité (existantes)
def load_config(file_path):
    """Load configuration from a JSON file."""
    with open(file_path, 'r') as file:
        config = json.load(file)
    return config

def save_config(config, file_path):
    """Save configuration to a JSON file."""
    with open(file_path, 'w') as file:
        json.dump(config, file, indent=4)