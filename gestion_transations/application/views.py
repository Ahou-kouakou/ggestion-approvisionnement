from django.shortcuts import render, redirect
#from .forms import TransactionForm

from django.core.paginator import Paginator
from .models import Transaction
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import CompteForm

@login_required
def dashboard_view(request):
    user = request.user
    filtre = request.GET.get('filtre')
    recherche = request.GET.get('recherche', '')

    transactions = Transaction.objects.none()  # Valeur par défaut

    # 💼 Si l'utilisateur est un client bancaire
    if user.user_type == 'client_bancaire':
        comptes_user = Compte.objects.filter(titulaire=user)
        transactions = Transaction.objects.filter(compte_credite__in=comptes_user)

    # 📡 Si l'utilisateur est un client opérateur
    elif user.user_type == 'client_operateur' and hasattr(user, 'operateur'):
        comptes_operateur = Compte.objects.filter(operateur=user.operateur)
        transactions = Transaction.objects.filter(compte_credite__in=comptes_operateur)

    # 👮 Si l'utilisateur est agent ou admin → accès global
    elif user.user_type in ['agent', 'admin']:
        transactions = Transaction.objects.all()

    # 🎯 Filtrage par statut
    if filtre == 'transmises':
        transactions = transactions.filter(statut='transmise')
    elif filtre == 'echouees':
        transactions = transactions.filter(statut='echec')

    # 🔍 Filtrage par recherche
    if recherche:
        transactions = transactions.filter(
            Q(compte_debite__titulaire__first_name__icontains=recherche) |
            Q(compte_debite__titulaire__last_name__icontains=recherche) |
            Q(compte_credite__titulaire__first_name__icontains=recherche) |
            Q(compte_credite__titulaire__last_name__icontains=recherche) |
            Q(reference_paiement__icontains=recherche)
        )

    # 📄 Pagination
    from django.core.paginator import Paginator
    paginator = Paginator(transactions.order_by('-date_transaction'), 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # 📊 Statistiques adaptées au filtrage
    total_transactions = transactions.count()
    total_transmises = transactions.filter(statut='transmise').count()
    total_echouees = transactions.filter(statut='echec').count()

    return render(request, 'dashboard.html', {
        'page_obj': page_obj,
        'filtre': filtre,
        'total_transactions': total_transactions,
        'total_transmises': total_transmises,
        'total_echouees': total_echouees,
        'recherche': recherche,
    })

def transaction_list_view(request):
    # Tu peux mettre une liste vide pour l'instant
    transactions = []
    return render(request, 'transaction_list.html', {'transactions': transactions})
    




from django.contrib.auth.forms import UserCreationForm

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from .models import Compte

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            # 👮 Agent connecté
            if request.user.is_authenticated and hasattr(request.user, 'user_type') and request.user.user_type == 'agent':
                if user.user_type == 'client_bancaire':
    # traitement pour client bancaire
                    user.save()
                    Compte.objects.create(
                        numero_compte=f"CMP-{user.id:04}",
                        solde=0,
                        type='banque',
                        titulaire=user
                    )
                    messages.success(request, "Le client et son compte ont été créés avec succès.")
                    return redirect('dashboard')
                else:
                    messages.error(request, "Un agent ne peut inscrire qu’un client.")
                    return redirect('register')

            # 👤 Utilisateur non connecté
            else:
                if user.user_type == 'client_bancaire':
    # traitement pour client bancaire
                    messages.error(request, "Vous devez être connecté comme agent pour inscrire un client.")
                    return redirect('login')
                else:
                    user.save()
                    messages.success(request, "Votre compte agent a été créé avec succès. Veuillez vous connecter.")
                    return redirect('login')

        else:
            messages.error(request, "Erreur dans le formulaire. Veuillez corriger les champs.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})



@login_required
def creer_compte_view(request):
    if request.method == 'POST':
        form = CompteForm(request.POST)
        if form.is_valid():
            compte = form.save(commit=False)
            compte.titulaire = request.user  # compte client
            compte.save()
            return redirect('dashboard')
    else:
        form = CompteForm()
    return render(request, 'compte/creer_compte.html', {'form': form})



from .models import Compte
from .forms import RechargementForm,ClientOperateurForm

@login_required
def recharger_compte_view(request):
    if request.user.user_type != 'agent':
        return render(request, 'compte/erreur.html', {'message': "Accès non autorisé."})

    if request.method == 'POST':
        form = RechargementForm(request.POST)
        if form.is_valid():
            compte = form.cleaned_data['compte']
            montant = form.cleaned_data['montant']
            compte.solde += montant
            compte.save()
            return redirect('dashboard')
    else:
        form = RechargementForm()

    return render(request, 'compte/rechargement.html', {'form': form})


from .forms import CompteOperateurForm

@login_required
def creer_compte_operateur(request):
    if request.method == 'POST':
        form = CompteOperateurForm(request.POST)
        if form.is_valid():
            compte = form.save(commit=False)
            compte.type = 'operateur'  # ✅ Forcer le type
            compte.titulaire = None     # ✅ S'assurer que seul l'opérateur est lié
            compte.save()
            messages.success(request, "Compte opérateur créé avec succès.")
            return redirect('dashboard')
        else:
            messages.error(request, "Erreur lors de la création du compte opérateur.")
    
    else:
        form = CompteOperateurForm()
    return render(request, 'compte/creer_compteO.html', {'form': form})



from django.contrib.auth import logout


def logout_view(request):
    logout(request)
    messages.success(request, "Vous avez été déconnecté avec succès.")
    return redirect('login')



from django.utils import timezone
from .models import Transaction
from .forms import TransactionForm
import uuid, os, csv
from django.conf import settings

from django.db import IntegrityError

from django.core.mail import send_mail
from django.utils import timezone
import requests
import uuid, os, csv
from django.conf import settings
from django.db import IntegrityError
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import TransactionForm
from .models import Transaction, Compte


@login_required
def creer_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.valide_par = request.user
            transaction.statut = Transaction.Statut.EN_ATTENTE
            transaction.date_transaction = timezone.now()
            transaction.reference_paiement = f"TRX-{uuid.uuid4().hex[:12].upper()}"

            compte_source = transaction.compte_debite
            compte_dest = transaction.compte_credite

            if compte_source.solde >= transaction.montant:
                try:
                    # 💸 Débit / Crédit
                    compte_source.solde -= transaction.montant
                    compte_dest.solde += transaction.montant
                    compte_source.save()
                    compte_dest.save()
                    transaction.save()

                    # 📝 Générer le fichier CSV
                    nom_fichier = f"{transaction.reference_paiement}.csv"
                    chemin = os.path.join(settings.DOSSIER_FICHIERS_CBS, nom_fichier)
                    transaction.nom_fichier = nom_fichier
                    transaction.save()

                    with open(chemin, 'w', newline='', encoding='utf-8') as f:
                        writer = csv.writer(f)
                        writer.writerow(['reference_paiement', 'montant', 'date', 'compte_client', 'compte_operateur'])
                        writer.writerow([
                            transaction.reference_paiement,
                            transaction.montant,
                            transaction.date_transaction.strftime("%Y-%m-%d %H:%M:%S"),
                            compte_source.numero_compte,
                            compte_dest.numero_compte
                        ])

                    # 🚀 Transmettre automatiquement à l’API
                    payload = {
                        "reference_paiement": transaction.reference_paiement,
                        "montant": str(transaction.montant),
                        "date_paiement": transaction.date_transaction.strftime("%Y-%m-%d %H:%M:%S"),
                        "code_client_mtn": compte_dest.numero_compte
                    }

                    try:
                        response = requests.post("https://httpbin.org/post", json=payload, timeout=5)
                        if response.status_code == 200:
                            transaction.statut = Transaction.Statut.TRANSMISE
                            transaction.date_transmission = timezone.now()
                            transaction.save()

                            # ✉️ Envoi du mail au client opérateur
                            if compte_dest.operateur and compte_dest.operateur.utilisateur:
                                destinataire = compte_dest.operateur.utilisateur.email
                                send_mail(
                                    subject="Notification : Votre compte a été crédité",
                                    message=(
                                        f"Bonjour,\n\n"
                                        f"Votre compte a été crédité d’un montant de {transaction.montant} FCFA.\n"
                                        f"Référence : {transaction.reference_paiement}\n"
                                        f"Date : {transaction.date_transaction.strftime('%d/%m/%Y à %H:%M')}\n\n"
                                        f"Merci pour votre confiance."
                                    ),
                                    from_email=settings.DEFAULT_FROM_EMAIL,
                                    recipient_list=[destinataire],
                                    fail_silently=False
                                )

                        else:
                            transaction.statut = Transaction.Statut.ECHEC
                            transaction.save()
                            messages.warning(request, f"⚠️ Transmission échouée (code {response.status_code})")

                    except Exception as e:
                        transaction.statut = Transaction.Statut.ECHEC
                        transaction.save()
                        messages.warning(request, f"⚠️ Erreur de transmission automatique : {str(e)}")

                    messages.success(request, f"✅ Transaction {transaction.reference_paiement} créée.")
                    return redirect('recu_transaction', transaction_id=transaction.id)

                except IntegrityError:
                    messages.error(request, "❌ Référence dupliquée. Réessayez.")
            else:
                messages.error(request, "❌ Solde insuffisant.")
        else:
            messages.error(request, "❌ Erreurs dans le formulaire.")
    else:
        form = TransactionForm()

    return render(request, 'transaction/formulaire_bordereau.html', {'form': form})


from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Transaction

@login_required
def recu_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    return render(request, 'transaction/recu_transaction.html', {'transaction': transaction})


from django.views.decorators.http import require_POST
from django.contrib import messages
import requests

@require_POST
@login_required

def retransmettre_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)

    if transaction.statut == Transaction.Statut.TRANSMISE:
        messages.info(request, f"La transaction {transaction.reference_paiement} a déjà été transmise.")
        return redirect('dashboard')


    # Construction des données à envoyer
    payload = {
        "reference_paiement": transaction.reference_paiement,
        "montant": str(transaction.montant),
        "date_paiement": transaction.date_transaction.strftime("%Y-%m-%d %H:%M:%S"),
        "code_client_mtn": transaction.compte_credite.numero_compte  # ou autre info spécifique
    }

    try:
        response = requests.post("https://httpbin.org/post", json=payload, timeout=5)
        if response.status_code == 200:
            transaction.statut = Transaction.Statut.TRANSMISE
            transaction.save()
            messages.success(request, f"✅ Transaction {transaction.reference_paiement} retransmise avec succès.")
        else:
            transaction.statut = Transaction.Statut.ECHEC
            transaction.save()
            messages.error(request, f"❌ Échec de retransmission. Code retour : {response.status_code}")
    except Exception as e:
        transaction.statut = Transaction.Statut.ECHEC
        transaction.save()
        messages.error(request, f"❌ Erreur lors de la retransmission : {str(e)}")

    return redirect('dashboard')




from django.http import JsonResponse
from django.views.decorators.http import require_GET
from .models import Transaction
from django.db.models import Q

from django.http import JsonResponse
from django.views.decorators.http import require_GET
from .models import Transaction
from django.db.models import Q

@require_GET
def api_transactions(request):
    # Récupérer les paramètres de filtrage et de recherche
    filtre = request.GET.get('filtre')
    recherche = request.GET.get('recherche', '')

    # Base de requête
    transactions = Transaction.objects.all().order_by('-date_transaction')

    # Appliquer les filtres
    if filtre:
        transactions = transactions.filter(statut=filtre.upper())

    # Appliquer la recherche
    if recherche:
        transactions = transactions.filter(
            Q(compte_debite__titulaire__first_name__icontains=recherche) |
            Q(compte_debite__titulaire__last_name__icontains=recherche) |
            Q(compte_credite__titulaire__first_name__icontains=recherche) |
            Q(compte_credite__titulaire__last_name__icontains=recherche) |
            Q(reference_paiement__icontains=recherche)
        )

    # Préparer les données
    data = []
    for trx in transactions:
        # Assurez-vous que tous les objets sont convertis en types de données simples
        compte_debite = f"{trx.compte_debite.titulaire.first_name} {trx.compte_debite.titulaire.last_name}" if trx.compte_debite.titulaire else str(trx.compte_debite.operateur)
        compte_credite = f"{trx.compte_credite.titulaire.first_name} {trx.compte_credite.titulaire.last_name}" if trx.compte_credite.titulaire else str(trx.compte_credite.operateur)

        data.append({
            "id": trx.id,
            "compteDebite": compte_debite,
            "soldeInitialDebite": float(trx.compte_debite.solde + trx.montant),
            "soldeFinalDebite": float(trx.compte_debite.solde),
            "compteCredite": compte_credite,
            "soldeInitialCredite": float(trx.compte_credite.solde - trx.montant),
            "soldeFinalCredite": float(trx.compte_credite.solde),
            "montant": float(trx.montant),
            "reference": trx.reference_paiement,
            "statut": trx.statut.lower(),
            "date": trx.date_transaction.strftime("%Y-%m-%d %H:%M:%S"),
            "motif": trx.motif if hasattr(trx, 'motif') else "",
            "frais": float(0)
        })

    return JsonResponse(data, safe=False)
#////

# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render
# from .models import Transaction, Compte

# @login_required
# def dashboard_client(request):
#     # Vérifier que l'utilisateur est un client
#     if hasattr(request.user, 'user_type') and request.user.user_type != 'client':
#         return redirect('/')  # Redirige vers une page autorisée ou d'erreur

#     # Récupérer le compte bancaire du client
#     compte_client = Compte.objects.filter(titulaire=request.user, type='banque').first()

#     # Si aucun compte n'existe, retourner un tableau vide
#     if not compte_client:
#         return render(request, 'dashboard_client.html', {
#             'transactions': [],
#             'compte': None
#         })

#     # Transactions reçues sur ce compte
#     transactions = Transaction.objects.filter(
#         compte_credite=compte_client
#     ).order_by('-date_transaction')

#     return render(request, 'dashboard_client.html', {
#         'transactions': transactions,
#         'compte': compte_client
#     })


# from django.contrib.auth.decorators import login_required
# from django.shortcuts import redirect

# @login_required
# def redirect_after_login(request):
#     if request.user.user_type == 'client':
#         return redirect('dashboard_client')  # Vue espace client
#     elif request.user.user_type == 'operateur':
#         return redirect('dashboard_operateur')  # Vue espace opérateur
#     else:
#         return redirect('admin:index')  # Par défaut, vers l'espace admin



@login_required
def mes_comptes_view(request):
    user = request.user

    # Clients bancaires → voir leurs propres comptes
    if user.user_type == 'client_bancaire':
        comptes = Compte.objects.filter(titulaire=user)

    # Clients opérateurs → voir comptes liés à leur opérateur
    elif user.user_type == 'client_operateur' and hasattr(user, 'operateur'):
        comptes = Compte.objects.filter(operateur=user.operateur)
    else:
        comptes = []

    return render(request, 'compte/mes_comptes.html', {'comptes': comptes})



from .models import Compte

@login_required
def creer_client_operateur(request):
    if request.user.user_type != 'agent':
        return redirect('dashboard')

    if request.method == 'POST':
        form = ClientOperateurForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = 'client_operateur'
            password = form.cleaned_data.get('password')
            user.set_password(password)
            user.save()

            # ✅ Création du compte pour ce client opérateur
            Compte.objects.create(
                type='operateur',
                titulaire=user
            )

            messages.success(request, "✅ Client opérateur créé avec son compte.")
            return redirect('dashboard')
    else:
        form = ClientOperateurForm()

    return render(request, 'utilisateur/creer_client_operateur.html', {'form': form})


@login_required
def espace_client_operateur(request):
    user = request.user
    try:
        compte = Compte.objects.get(titulaire=request.user)
        transactions = compte.transactions.order_by('-date')
    except Compte.DoesNotExist:
        compte = None
        transactions = []

    context = {
        'compte': compte,
        'transactions': transactions,
    }
    return render(request, 'utilisateur/dashboard.html', context)


# from .forms import TransactionForm
# from django.db import transaction as db_transaction  # transaction db pour atomicité

# @login_required
# def creer_transaction(request):
#     if request.method == 'POST':
#         form = TransactionForm(request.POST)
#         if form.is_valid():
#             compte_debite = form.cleaned_data['compte_debite']
#             client_operateur = form.cleaned_data['client_operateur']
#             montant = form.cleaned_data['montant']

#             try:
#                 compte_credite = Compte.objects.get(type='operateur', titulaire=client_operateur)
#             except Compte.DoesNotExist:
#                 messages.error(request, "❌ Le client opérateur n’a pas de compte.")
#                 return redirect('creer_transaction')

#             if compte_debite.solde < montant:
#                 messages.error(request, "❌ Solde insuffisant.")
#                 return redirect('creer_transaction')

#             # ✅ Bloc atomique pour garantir la cohérence des soldes
#             with db_transaction.atomic():
#                 compte_debite.solde -= montant
#                 compte_credite.solde += montant
#                 compte_debite.save()
#                 compte_credite.save()

#                 transaction = Transaction.objects.create(
#                     compte_debite=compte_debite,
#                     compte_credite=compte_credite,
#                     montant=montant,
#                     valide_par=request.user,
#                 )

#             messages.success(request, f"✅ Transaction créée : {transaction.reference_paiement}")
#             return redirect('creer_transaction')
#     else:
#         form = TransactionForm()

#     return render(request, 'transaction/creer_transaction.html', {'form': form})



import requests

import requests

def retransmettre_api(transaction):
    url_api = "https://httpbin.org/post"  # Remplace par l’URL réelle

    data = {
        "reference_paiement": transaction.reference_paiement,
        "date_paiement": transaction.date_transaction.isoformat(),  # Utilisation correcte du champ
        "montant": float(transaction.montant),  # envoi en float si API JSON attend ça
        #"code_client_mtn": transaction.compte_credite.code_client_mtn,  # Je suppose que code_client_mtn est lié au compte crédité
    }

    try:
        response = requests.post(url_api, json=data, timeout=10)
        return response.status_code == 200
    except Exception as e:
        print(f"Erreur retransmission : {e}")
        return False

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from application.models import Transaction
@csrf_exempt
@csrf_exempt
def retransmettre_transaction(request, id):
    if request.method == 'POST':
        try:
            tx = Transaction.objects.get(id=id)
            success = retransmettre_api(tx)

            if success:
                tx.statut = 'transmise'
                tx.date_transmission = timezone.now()
                tx.save()

                # ✅ Envoi de mail au client opérateur
                if tx.compte_credite.operateur and tx.compte_credite.operateur.utilisateur:
                    email = tx.compte_credite.operateur.utilisateur.email
                    send_mail(
                        subject="Notification : Crédit de votre compte",
                        message=(
                            f"Bonjour,\n\n"
                            f"Votre compte a été crédité avec succès.\n"
                            f"Montant : {tx.montant} FCFA\n"
                            f"Référence : {tx.reference_paiement}\n"
                            f"Date : {tx.date_transaction.strftime('%d/%m/%Y à %H:%M')}\n\n"
                            f"Merci de votre collaboration."
                        ),
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[email],
                        fail_silently=False
                    )

                return JsonResponse({'status': 'success', 'message': 'Retransmission réussie + email envoyé'})

            else:
                return JsonResponse({'status': 'error', 'message': 'Échec de la retransmission'}, status=400)

        except Transaction.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Transaction introuvable'}, status=404)

    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée'}, status=405)
