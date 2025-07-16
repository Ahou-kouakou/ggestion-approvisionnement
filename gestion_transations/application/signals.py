from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Transaction, Compte, CustomUser

@receiver(post_save, sender=Transaction)
def envoyer_notification_credit(sender, instance, created, **kwargs):
    # Envoyer le mail si le statut est "transmise" ET qu'on n'a pas encore envoyé la notification
    if instance.statut == "transmise" and not instance.notification_envoyee:
        compte_credite = instance.compte_credite
        client = compte_credite.titulaire

        # Vérifie que le compte crédité appartient bien à un client opérateur
        if client and client.user_type == "client_operateur":
            montant = instance.montant
            nouveau_solde = compte_credite.solde
            numero_compte = compte_credite.numero_compte

            # Nom de l’émetteur
            compte_debite = instance.compte_debite
            emetteur = compte_debite.titulaire
            nom_emetteur = f"{emetteur.first_name} {emetteur.last_name}" if emetteur else "Inconnu"

            try:
                send_mail(
                    subject='📩 Crédit effectué sur votre compte',
                    message=f"""
Bonjour {client.first_name},

Nous vous informons que votre compte {numero_compte} a été crédité de {montant} FCFA.

🧾 Référence de la transaction : {instance.reference_paiement}  
💳 Émetteur : {nom_emetteur}  
💰 Nouveau solde : {nouveau_solde} FCFA

Merci de votre confiance.

Cordialement,  
Votre Banque
""",
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[client.email],
                    fail_silently=False
                )

                # Marquer que la notification a été envoyée
                instance.notification_envoyee = True
                instance.save(update_fields=["notification_envoyee"])

            except Exception as e:
                print("Erreur lors de l'envoi de l'e-mail :", e)
