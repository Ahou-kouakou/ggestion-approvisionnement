# from django import forms
# from .models import Transaction

# class TransactionForm(forms.ModelForm):
#     class Meta:
#         model = Transaction
#         fields = [
#             'montant',
#             'compte_emetteur',
#             'compte_beneficiaire',
#             'libelle',
#         ]
#         labels = {
#             'montant': 'Montant',
#             'compte_emetteur': 'Compte à débiter',
#             'compte_beneficiaire': 'Compte à créditer',
#             'libelle': 'Libellé',
#         }

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.contrib.auth.forms import AuthenticationForm

class CustomLoginForm(AuthenticationForm):
    username = forms.EmailField(label="Adresse email", widget=forms.EmailInput(attrs={'autofocus': True}))


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(label="Prénom", required=True)
    last_name = forms.CharField(label="Nom", required=True)
    email = forms.EmailField(label="Adresse Email", required=True)
    telephone = forms.CharField(label="Téléphone", required=True)
    user_type = forms.ChoiceField(label="Type d'utilisateur", choices=CustomUser.TYPE_CHOICES)
    password1 = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirmer le mot de passe", widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'telephone', 'user_type', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.telephone = self.cleaned_data['telephone']
        user.user_type = self.cleaned_data['user_type']
        if commit:
            user.save()
        return user




from django import forms
from .models import Compte

class CompteForm(forms.ModelForm):
    class Meta:
        model = Compte
        fields = ['numero_compte', 'solde', 'type']
        labels = {
            'numero_compte': 'Numéro de compte',
            'solde': 'Solde initial',
            'type': 'Type de compte',
        }
        widgets = {
            'numero_compte': forms.TextInput(attrs={'class': 'form-control'}),
            'solde': forms.NumberInput(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
        }





class RechargementForm(forms.Form):
    compte = forms.ModelChoiceField(
        queryset=Compte.objects.filter(type='banque'),
        label="Compte à recharger"
    )
    montant = forms.DecimalField(max_digits=10, decimal_places=2, min_value=0, label="Montant à ajouter")



from django import forms
from .models import Compte, Operateur

class CompteOperateurForm(forms.ModelForm):
    class Meta:
        model = Compte
        fields = ['numero_compte', 'solde', 'operateur']  # ❌ on enlève 'titulaire'
        labels = {
            'numero_compte': "Numéro du compte",
            'solde': "Solde initial",
            'operateur': "Opérateur mobile"
        }

    def save(self, commit=True):
        compte = super().save(commit=False)
        compte.type = 'operateur'     # ✅ Fixer le type opérateur
        compte.titulaire = None       # ✅ S'assurer que le titulaire est vide
        if commit:
            compte.save()
        return compte




from django import forms
from .models import Transaction, Compte

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['montant', 'compte_debite', 'compte_credite']
        labels = {
            'montant': "Montant à transférer",
            'compte_debite': "Compte bancaire à débiter",
            'compte_credite': "Compte opérateur à créditer",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Limiter la sélection aux comptes bancaires (type = banque)
        self.fields['compte_debite'].queryset = Compte.objects.filter(type='banque')
        self.fields['compte_debite'].label_from_instance = lambda obj: f"{obj.numero_compte} – {obj.titulaire.get_full_name()}"

        # Limiter aux comptes opérateur (type = operateur)
        self.fields['compte_credite'].queryset = Compte.objects.filter(type='operateur')
        self.fields['compte_credite'].label_from_instance = lambda obj: f"{obj.numero_compte} – {obj.operateur.nom}"
