#!/usr/bin/env python3
"""
Script de test et d'exemple d'utilisation du gestionnaire d'annuaire.
"""

from main import AnnuaireManager

def main():
    # Créer une instance du gestionnaire
    annuaire = AnnuaireManager()
    
    print("=" * 50)
    print("ANNUAIRE TÉLÉPHONIQUE - EXEMPLE D'UTILISATION")
    print("=" * 50)
    
    # 1. Ajouter des contacts
    print("\n1️⃣  AJOUT DE CONTACTS")
    print("-" * 50)
    
    contact1 = annuaire.ajouter_contact(
        nom="Dupont",
        prenom="Jean",
        email="jean.dupont@example.com",
        telephone="06 12 34 56 78",
        adresse="123 rue de Paris, 75000 Paris",
        adresse_travail="456 avenue de l'Industrie, 92000 Nanterre"
    )
    print(f"✅ Contact ajouté: {contact1['prenom']} {contact1['nom']} (ID: {contact1['id']})")
    
    contact2 = annuaire.ajouter_contact(
        nom="Martin",
        prenom="Sophie",
        email="sophie.martin@example.com",
        telephone="07 98 76 54 32",
        adresse="789 boulevard Saint-Germain, 75005 Paris",
        adresse_travail="200 rue de Rivoli, 75001 Paris"
    )
    print(f"✅ Contact ajouté: {contact2['prenom']} {contact2['nom']} (ID: {contact2['id']})")
    
    contact3 = annuaire.ajouter_contact(
        nom="Bernard",
        prenom="Pierre",
        email="pierre.bernard@example.com",
        telephone="06 55 44 33 22",
        adresse="321 rue Rivoli, 75002 Paris",
        adresse_travail="789 avenue Champs-Élysées, 75008 Paris"
    )
    print(f"✅ Contact ajouté: {contact3['prenom']} {contact3['nom']} (ID: {contact3['id']})")
    
    # 2. Afficher tous les contacts
    print("\n2️⃣  TOUS LES CONTACTS")
    print("-" * 50)
    tous_contacts = annuaire.obtenir_tous_les_contacts()
    for contact in tous_contacts:
        print(f"  • {contact['prenom']} {contact['nom']} | {contact['telephone']} | {contact['email']}")
    
    # 3. Obtenir un contact par ID
    print("\n3️⃣  RECHERCHER PAR ID")
    print("-" * 50)
    contact = annuaire.obtenir_contact_par_id(1)
    if contact:
        print(f"Contact trouvé:")
        print(f"  Nom: {contact['nom']} {contact['prenom']}")
        print(f"  Email: {contact['email']}")
        print(f"  Téléphone: {contact['telephone']}")
        print(f"  Adresse: {contact['adresse']}")
        print(f"  Adresse travail: {contact['adresse_travail']}")
    
    # 4. Rechercher des contacts
    print("\n4️⃣  RECHERCHE DE CONTACTS")
    print("-" * 50)
    resultats = annuaire.rechercher_contacts("Martin")
    print(f"Recherche pour 'Martin': {len(resultats)} résultat(s)")
    for contact in resultats:
        print(f"  • {contact['prenom']} {contact['nom']} | {contact['email']}")
    
    # 5. Modifier un contact
    print("\n5️⃣  MODIFICATION D'UN CONTACT")
    print("-" * 50)
    contact_modifie = annuaire.modifier_contact(1, telephone="06 99 88 77 66")
    print(f"✅ Contact ID {contact_modifie['id']} modifié")
    print(f"  Nouveau téléphone: {contact_modifie['telephone']}")
    
    # 6. Afficher les statistiques
    print("\n6️⃣  STATISTIQUES")
    print("-" * 50)
    stats = annuaire.obtenir_stats()
    print(f"Total de contacts: {stats['total_contacts']}")
    print(f"Consultation: {stats['date_consultation']}")
    
    # 7. Supprimer un contact
    print("\n7️⃣  SUPPRESSION D'UN CONTACT")
    print("-" * 50)
    if annuaire.supprimer_contact(3):
        print("✅ Contact ID 3 supprimé")
    
    print(f"Nombre de contacts après suppression: {len(annuaire.obtenir_tous_les_contacts())}")
    
    print("\n" + "=" * 50)
    print("✅ Exemple terminé! Les données sont sauvegardées dans 'contacts.json'")
    print("=" * 50)

if __name__ == "__main__":
    main()
