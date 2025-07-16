import time
import os
import csv
import requests  # type: ignore
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from application.models import Transaction

def envoyer_mail_credit(transaction):
    try:
        compte_dest = transaction.compte_credite
        if compte_dest.operateur and compte_dest.operateur.utilisateur:
            destinataire = compte_dest.operateur.utilisateur.email
            send_mail(
                subject="✅ Crédit sur votre compte opérateur",
                message=(
                    f"Bonjour,\n\n"
                    f"Votre compte a été crédité d’un montant de {transaction.montant} FCFA.\n"
                    f"Référence : {transaction.reference_paiement}\n"
                    f"Date : {transaction.date_transaction.strftime('%d/%m/%Y à %H:%M')}\n\n"
                    f"Cordialement,\nVotre banque."
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[destinataire],
                fail_silently=False
            )
            print(f"[EMAIL] Mail envoyé à {destinataire}")
    except Exception as e:
        print(f"[EMAIL-ERREUR] {e}")

class FichierCBSEventHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory or not event.src_path.endswith('.csv'):
            return

        print(f"[DETECTION] Nouveau fichier : {event.src_path}")
        try:
            with open(event.src_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for ligne in reader:
                    reference = ligne.get('reference_paiement')
                    montant = ligne.get('montant')
                    compte_client = ligne.get('compte_client')
                    compte_operateur = ligne.get('compte_operateur')

                    # Appel API (exemple fictif)
                    response = requests.post("https://httpbin.org/post", json={
                        "reference": reference,
                        "montant": montant,
                        "client": compte_client,
                        "operateur": compte_operateur
                    })

                    statut = "transmise" if response.status_code == 200 else "echec"

                    # Mise à jour de la transaction
                    tx = Transaction.objects.filter(reference_paiement=reference).first()
                    if tx:
                        tx.statut = statut
                        tx.date_transmission = timezone.now()
                        tx.save()

                        # ✅ Envoi du mail seulement si TRANSMISE
                        if statut == "transmise":
                            envoyer_mail_credit(tx)

                    print(f"[API] {reference} → {statut.upper()}")
        except Exception as e:
            print(f"[ERREUR] {e}")

def start_file_watcher():
    dossier = settings.DOSSIER_FICHIERS_CBS
    observer = Observer()
    event_handler = FichierCBSEventHandler()
    observer.schedule(event_handler, path=str(dossier), recursive=False)
    observer.start()
    print(f"[SURVEILLANCE] Dossier : {dossier}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
