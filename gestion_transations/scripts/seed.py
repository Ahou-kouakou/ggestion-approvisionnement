import os
import sys
import django
import random
from datetime import datetime, timedelta

# Configuration Django
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gestion_transations.settings")
django.setup()

from django.contrib.auth import get_user_model
from application.models import Compte, Transaction, Operateur
import uuid
import csv
from django.conf import settings
from django.db import IntegrityError

User = get_user_model()

# Données réalistes
prenoms = ['Aïcha', 'Aminata', 'Fatou', 'Mariam', 'Ramatoulaye', 
          'Abdoulaye', 'Amadou', 'Moussa', 'Ousmane', 'Cheikh']
noms = ['Diop', 'Traoré', 'Touré', 'Diallo', 'Ndiaye',
       'Sow', 'Kane', 'Gueye', 'Fall', 'Ba']

def generate_unique_email(first_name, last_name):
    """Génère un email unique"""
    base_email = f"{first_name.lower()}.{last_name.lower()}@bank.sn"
    email = base_email
    counter = 1
    
    while User.objects.filter(email=email).exists():
        email = f"{base_email.split('@')[0]}{counter}@bank.sn"
        counter += 1
    
    return email

def create_users():
    """Crée des utilisateurs avec emails uniques"""
    users = []
    for i in range(10):
        first_name = random.choice(prenoms)
        last_name = random.choice(noms)
        
        try:
            user = User.objects.create(
                email=generate_unique_email(first_name, last_name),
                first_name=first_name,
                last_name=last_name,
                telephone=f"77{random.randint(1000000, 9999999)}",
                user_type=random.choice(['client', 'agent', 'admin']),
            )
            user.set_password('Passer123!')
            user.save()
            users.append(user)
            print(f"Utilisateur créé : {user.email}")
        except IntegrityError as e:
            print(f"Erreur création utilisateur: {e}")
            continue
            
    return users

def create_operateurs():
    operateurs = [
        {'nom': 'Orange Money', 'type': 'mobile money', 'adresse': 'Dakar'},
        {'nom': 'Wave', 'type': 'mobile money', 'adresse': 'Dakar'},
        {'nom': 'Wari', 'type': 'mobile money', 'adresse': 'Dakar'},
    ]
    return [Operateur.objects.get_or_create(**op)[0] for op in operateurs]

def create_comptes(users, operateurs):
    comptes = []
    for user in users:
        # Compte bancaire
        try:
            compte = Compte.objects.create(
                titulaire=user,
                solde=random.randint(50000, 5000000),
                type='banque'
            )
            comptes.append(compte)
        except IntegrityError as e:
            print(f"Erreur création compte: {e}")
            continue
        
        # Compte opérateur (50% de chance)
        if random.choice([True, False]):
            try:
                compte_op = Compte.objects.create(
                    operateur=random.choice(operateurs),
                    solde=random.randint(1000, 500000),
                    type='operateur'
                )
                comptes.append(compte_op)
            except IntegrityError as e:
                print(f"Erreur création compte opérateur: {e}")
                continue
    return comptes

def generate_unique_reference():
    """Génère une référence de paiement unique"""
    while True:
        ref = f"TRX-{uuid.uuid4().hex[:8].upper()}"
        if not Transaction.objects.filter(reference_paiement=ref).exists():
            return ref

def create_transactions(comptes):
    DOSSIER_FICHIERS_CBS = getattr(settings, "DOSSIER_FICHIERS_CBS", os.path.join(BASE_DIR, "fichiers_cbs"))
    os.makedirs(DOSSIER_FICHIERS_CBS, exist_ok=True)

    for _ in range(50):
        debite = random.choice(comptes)
        credite = random.choice([c for c in comptes if c != debite])
        montant = random.randint(1000, 200000)
        
        try:
            trx = Transaction.objects.create(
                compte_debite=debite,
                compte_credite=credite,
                montant=montant,
                statut=random.choice(['attente', 'transmise', 'echec']),
                reference_paiement=generate_unique_reference()
            )
            
            # Fichier CBS
            nom_fichier = f"{trx.reference_paiement}.csv"
            with open(os.path.join(DOSSIER_FICHIERS_CBS, nom_fichier), 'w') as f:
                writer = csv.writer(f, delimiter='|')
                writer.writerow(['Reference', 'Montant', 'Compte_Debit', 'Compte_Credit'])
                writer.writerow([trx.reference_paiement, trx.montant, debite.numero_compte, credite.numero_compte])
            
            trx.nom_fichier = nom_fichier
            trx.save()
            print(f"Transaction {trx.reference_paiement} créée")
            
        except IntegrityError as e:
            print(f"Erreur création transaction: {e}")
            continue

if __name__ == "__main__":
    print("Nettoyage des anciennes données...")
    Transaction.objects.all().delete()
    Compte.objects.all().delete()
    User.objects.filter(is_superuser=False).delete()
    Operateur.objects.all().delete()
    
    print("\nCréation des utilisateurs...")
    users = create_users()
    
    print("\nCréation des opérateurs...")
    operateurs = create_operateurs()
    
    print("\nCréation des comptes...")
    comptes = create_comptes(users, operateurs)
    
    print("\nCréation des transactions...")
    create_transactions(comptes)
    
    print("\n✅ Données créées avec succès!")
    print(f"Utilisateurs: {User.objects.count()}")
    print(f"Comptes: {Compte.objects.count()}")
    print(f"Transactions: {Transaction.objects.count()}")