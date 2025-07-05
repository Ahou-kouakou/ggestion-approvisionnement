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
    filtre = request.GET.get('filtre', 'toutes')
    recherche = request.GET.get('recherche', '')

    transactions = Transaction.objects.all()

    # Filtrage par statut
    if filtre == 'transmises':
        transactions = transactions.filter(statut='TRANSMISE')
    elif filtre == 'echouees':
        transactions = transactions.filter(statut='ECHEC')

    # Filtrage par recherche (nom, prénom, référence)
    if recherche:
        transactions = transactions.filter(
            Q(compte_debite__titulaire__first_name__icontains=recherche) |
            Q(compte_debite__titulaire__last_name__icontains=recherche) |
            Q(compte_credite__titulaire__first_name__icontains=recherche) |
            Q(compte_credite__titulaire__last_name__icontains=recherche) |
            Q(reference_paiement__icontains=recherche)
        )

    # Pagination
    from django.core.paginator import Paginator
    paginator = Paginator(transactions.order_by('-date_transaction'), 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Statistiques
    total_transactions = Transaction.objects.count()
    total_transmises = Transaction.objects.filter(statut='TRANSMISE').count()
    total_echouees = Transaction.objects.filter(statut='ECHEC').count()

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
    

# def transaction_form_view(request):
#     if request.method == 'POST':
#         form = TransactionForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('dashboard')  # redirection après validation
#     else:
#         form = TransactionForm()

#     return render(request, 'transaction_form.html', {'form': form})



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
                if user.user_type == 'client':
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
                if user.user_type == 'client':
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
from .forms import RechargementForm

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

@login_required
def creer_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.valide_par = request.user
            transaction.statut = Transaction.Statut.EN_ATTENTE
            transaction.date_transaction = timezone.now()
            transaction.reference_paiement = f"TRX-{uuid.uuid4().hex[:12].upper()}"  # Génération

            compte_source = transaction.compte_debite
            compte_dest = transaction.compte_credite

            if compte_source.solde >= transaction.montant:
                try:
                    # Débit / Crédit
                    compte_source.solde -= transaction.montant
                    compte_dest.solde += transaction.montant

                    compte_source.save()
                    compte_dest.save()
                    transaction.save()

                    # Générer le fichier CSV
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

    # Afficher le formulaire en GET ou en cas d’erreur
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