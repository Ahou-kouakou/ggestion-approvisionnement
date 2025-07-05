import time
import os
import csv
import requests # type: ignore
from django.utils import timezone
from django.conf import settings
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from application.models import Transaction

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
