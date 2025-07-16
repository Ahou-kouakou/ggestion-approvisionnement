from django.core.mail import send_mail
from django.conf import settings

def send_notification_email(user_email, montant, nouveau_solde):
    subject = "Notification de crédit sur votre compte"
    message = (
        f"Bonjour,\n\n"
        f"Votre compte a été crédité d'un montant de {montant}.\n"
        f"Votre nouveau solde est de {nouveau_solde}.\n\n"
        f"Cordialement,\n"
        f"L'équipe de gestion des transactions"
    )
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user_email]

    send_mail(subject, message, from_email, recipient_list)
