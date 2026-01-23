#!/usr/bin/env python3
"""
Interface interactive en terminal pour l'annuaire téléphonique.
"""

import os
import sys
from main import AnnuaireManager

def clear_screen():
    """Efface l'écran du terminal."""
    os.system('clear' if os.name == 'posix' else 'cls')

def afficher_menu():
    """Affiche le menu principal."""
    print("\n" + "="*60)
    print("📞 ANNUAIRE TÉLÉPHONIQUE")
    print("="*60)
    print("1. ➕  Ajouter un contact")
    print("2. 📋 Afficher tous les contacts")
    print("3. 🔍 Rechercher un contact")
    print("4. 👁️  Voir les détails d'un contact")
    print("5. ✏️  Modifier un contact")
    print("6. 🗑️  Supprimer un contact")
    print("7. 📊 Statistiques")
    print("0. ❌ Quitter")
    print("="*60)
    return input("Choisissez une option (0-7): ").strip()

def ajouter_contact(annuaire):
    """Interface pour ajouter un contact."""
    clear_screen()
    print("\n➕ AJOUTER UN NOUVEAU CONTACT")
    print("-"*60)
    
    try:
        nom = input("Nom: ").strip()
        if not nom:
            print("❌ Le nom est requis!")
            return
        
        prenom = input("Prénom: ").strip()
        if not prenom:
            print("❌ Le prénom est requis!")
            return
        
        email = input("Email: ").strip()
        if not email:
            print("❌ L'email est requis!")
            return
        
        telephone = input("Téléphone: ").strip()
        if not telephone:
            print("❌ Le téléphone est requis!")
            return
        
        adresse = input("Adresse: ").strip()
        if not adresse:
            print("❌ L'adresse est requise!")
            return
        
        adresse_travail = input("Adresse de travail: ").strip()
        if not adresse_travail:
            print("❌ L'adresse de travail est requise!")
            return
        
        contact = annuaire.ajouter_contact(nom, prenom, email, telephone, adresse, adresse_travail)
        print(f"\n✅ Contact ajouté avec succès!")
        print(f"   ID: {contact['id']}")
        print(f"   {contact['prenom']} {contact['nom']}")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    input("\nAppuyez sur Entrée pour continuer...")

def afficher_tous_contacts(annuaire):
    """Affiche tous les contacts."""
    clear_screen()
    print("\n📋 TOUS LES CONTACTS")
    print("-"*60)
    
    contacts = annuaire.obtenir_tous_les_contacts()
    
    if not contacts:
        print("❌ Aucun contact dans l'annuaire.")
    else:
        print(f"\n{'ID':<4} {'Prénom':<15} {'Nom':<15} {'Téléphone':<15}")
        print("-"*60)
        for contact in contacts:
            print(f"{contact['id']:<4} {contact['prenom']:<15} {contact['nom']:<15} {contact['telephone']:<15}")
        print(f"\n📊 Total: {len(contacts)} contact(s)")
    
    input("\nAppuyez sur Entrée pour continuer...")

def rechercher_contact(annuaire):
    """Recherche des contacts."""
    clear_screen()
    print("\n🔍 RECHERCHER UN CONTACT")
    print("-"*60)
    
    terme = input("Entrez un terme de recherche (nom, prénom ou email): ").strip()
    
    if not terme:
        print("❌ Veuillez entrer un terme de recherche!")
        input("\nAppuyez sur Entrée pour continuer...")
        return
    
    resultats = annuaire.rechercher_contacts(terme)
    
    if not resultats:
        print(f"❌ Aucun contact trouvé pour '{terme}'")
    else:
        print(f"\n✅ {len(resultats)} résultat(s) trouvé(s):\n")
        print(f"{'ID':<4} {'Prénom':<15} {'Nom':<15} {'Email':<25}")
        print("-"*60)
        for contact in resultats:
            print(f"{contact['id']:<4} {contact['prenom']:<15} {contact['nom']:<15} {contact['email']:<25}")
    
    input("\nAppuyez sur Entrée pour continuer...")

def voir_details_contact(annuaire):
    """Affiche les détails d'un contact."""
    clear_screen()
    print("\n👁️  DÉTAILS D'UN CONTACT")
    print("-"*60)
    
    try:
        contact_id = int(input("Entrez l'ID du contact: ").strip())
        contact = annuaire.obtenir_contact_par_id(contact_id)
        
        if not contact:
            print(f"❌ Contact avec l'ID {contact_id} non trouvé!")
        else:
            print(f"\n{'='*60}")
            print(f"{'📌 DÉTAILS DU CONTACT':^60}")
            print(f"{'='*60}")
            print(f"ID:               {contact['id']}")
            print(f"Prénom:           {contact['prenom']}")
            print(f"Nom:              {contact['nom']}")
            print(f"Email:            {contact['email']}")
            print(f"Téléphone:        {contact['telephone']}")
            print(f"Adresse:          {contact['adresse']}")
            print(f"Adresse travail:  {contact['adresse_travail']}")
            print(f"Créé le:          {contact.get('date_creation', 'N/A')}")
            if 'date_modification' in contact:
                print(f"Modifié le:       {contact['date_modification']}")
            print(f"{'='*60}")
    
    except ValueError:
        print("❌ Veuillez entrer un ID valide!")
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    input("\nAppuyez sur Entrée pour continuer...")

def modifier_contact(annuaire):
    """Modifie un contact."""
    clear_screen()
    print("\n✏️  MODIFIER UN CONTACT")
    print("-"*60)
    
    try:
        contact_id = int(input("Entrez l'ID du contact à modifier: ").strip())
        contact = annuaire.obtenir_contact_par_id(contact_id)
        
        if not contact:
            print(f"❌ Contact avec l'ID {contact_id} non trouvé!")
            input("\nAppuyez sur Entrée pour continuer...")
            return
        
        print(f"\nContact actuel: {contact['prenom']} {contact['nom']}")
        print("-"*60)
        print("Laissez vide pour garder la valeur actuelle\n")
        
        nouveau_nom = input(f"Nom ({contact['nom']}): ").strip()
        nouveau_prenom = input(f"Prénom ({contact['prenom']}): ").strip()
        nouvel_email = input(f"Email ({contact['email']}): ").strip()
        nouveau_telephone = input(f"Téléphone ({contact['telephone']}): ").strip()
        nouvelle_adresse = input(f"Adresse ({contact['adresse']}): ").strip()
        nouvelle_adresse_travail = input(f"Adresse travail ({contact['adresse_travail']}): ").strip()
        
        # Créer un dictionnaire avec seulement les champs modifiés
        modifications = {}
        if nouveau_nom:
            modifications['nom'] = nouveau_nom
        if nouveau_prenom:
            modifications['prenom'] = nouveau_prenom
        if nouvel_email:
            modifications['email'] = nouvel_email
        if nouveau_telephone:
            modifications['telephone'] = nouveau_telephone
        if nouvelle_adresse:
            modifications['adresse'] = nouvelle_adresse
        if nouvelle_adresse_travail:
            modifications['adresse_travail'] = nouvelle_adresse_travail
        
        if not modifications:
            print("❌ Aucune modification n'a été effectuée.")
        else:
            contact_modifie = annuaire.modifier_contact(contact_id, **modifications)
            print(f"\n✅ Contact modifié avec succès!")
            print(f"   {contact_modifie['prenom']} {contact_modifie['nom']}")
    
    except ValueError:
        print("❌ Veuillez entrer un ID valide!")
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    input("\nAppuyez sur Entrée pour continuer...")

def supprimer_contact(annuaire):
    """Supprime un contact."""
    clear_screen()
    print("\n🗑️  SUPPRIMER UN CONTACT")
    print("-"*60)
    
    try:
        contact_id = int(input("Entrez l'ID du contact à supprimer: ").strip())
        contact = annuaire.obtenir_contact_par_id(contact_id)
        
        if not contact:
            print(f"❌ Contact avec l'ID {contact_id} non trouvé!")
            input("\nAppuyez sur Entrée pour continuer...")
            return
        
        print(f"\n⚠️  Vous êtes sur le point de supprimer:")
        print(f"    {contact['prenom']} {contact['nom']}")
        confirmation = input("\nConfirmez la suppression (oui/non): ").strip().lower()
        
        if confirmation == 'oui' or confirmation == 'o':
            if annuaire.supprimer_contact(contact_id):
                print(f"\n✅ Contact supprimé avec succès!")
            else:
                print(f"❌ Erreur lors de la suppression!")
        else:
            print("❌ Suppression annulée.")
    
    except ValueError:
        print("❌ Veuillez entrer un ID valide!")
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    input("\nAppuyez sur Entrée pour continuer...")

def afficher_statistiques(annuaire):
    """Affiche les statistiques."""
    clear_screen()
    print("\n📊 STATISTIQUES")
    print("-"*60)
    
    stats = annuaire.obtenir_stats()
    print(f"Total de contacts: {stats['total_contacts']}")
    print(f"Consultation: {stats['date_consultation']}")
    
    input("\nAppuyez sur Entrée pour continuer...")

def main():
    """Fonction principale."""
    annuaire = AnnuaireManager()
    
    while True:
        clear_screen()
        option = afficher_menu()
        
        if option == '0':
            clear_screen()
            print("\n👋 Au revoir!")
            sys.exit(0)
        elif option == '1':
            ajouter_contact(annuaire)
        elif option == '2':
            afficher_tous_contacts(annuaire)
        elif option == '3':
            rechercher_contact(annuaire)
        elif option == '4':
            voir_details_contact(annuaire)
        elif option == '5':
            modifier_contact(annuaire)
        elif option == '6':
            supprimer_contact(annuaire)
        elif option == '7':
            afficher_statistiques(annuaire)
        else:
            print("❌ Option invalide! Veuillez choisir entre 0 et 7.")
            input("\nAppuyez sur Entrée pour continuer...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        clear_screen()
        print("\n👋 Annuaire fermé par l'utilisateur.")
        sys.exit(0)
