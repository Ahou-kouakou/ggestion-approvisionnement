from django.db import models
from django.conf import settings
from django.utils import timezone
import uuid

from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class CustomUser(AbstractUser):
    username = None  # désactive le champ username
    email = models.EmailField(max_length=150, unique=True, verbose_name="Adresse Email")
    telephone = models.CharField(
    max_length=10,
    validators=[RegexValidator(r'^\d{10}$', 'Entrez un numéro de téléphone valide à 10 chiffres.')],
    verbose_name="Téléphone"
)
#/////////
    TYPE_CHOICES = (
    ('client_bancaire', 'Client bancaire'),
    ('client_operateur', 'Client opérateur'),
    ('agent', 'Agent'),
    ('admin', 'Administrateur'),
)

    user_type = models.CharField(max_length=16, choices=TYPE_CHOICES, default='client', verbose_name="Type d'utilisateur")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'telephone', 'user_type']
    

    def __str__(self):
        return f"{self.email} ({self.user_type})"



# ------------------------------------------------------------------
#  OPERATEUR
# ------------------------------------------------------------------
class Operateur(models.Model):
    nom      = models.CharField(max_length=50, unique=True)
    type     = models.CharField(max_length=50)            # « mobile money », « telco », …
    adresse  = models.CharField(max_length=200)
    #//////
    utilisateur = models.OneToOneField(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    null=True, blank=True,
    related_name='operateur'
)


    def __str__(self):
        return self.nom


# ------------------------------------------------------------------
#   COMPTE
# ------------------------------------------------------------------
class Compte(models.Model):
    class TypeCompte(models.TextChoices):
        BANQUE    = 'banque',    'Banque'
        OPERATEUR = 'operateur', 'Opérateur'

    # 🔁 on rend ce champ facultatif dans le formulaire
    numero_compte = models.CharField(max_length=30, unique=True, blank=True)
    solde         = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    type          = models.CharField(max_length=10, choices=TypeCompte.choices)

    titulaire     = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='comptes'
    )
    operateur     = models.ForeignKey(
        Operateur,
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='comptes'
    )

    def save(self, *args, **kwargs):
        # ✅ Génération automatique du numéro de compte
        if not self.numero_compte:
            prefix = "CMP" if self.type == "banque" else "OPR"
            uid = uuid.uuid4().hex[:6].upper()
            self.numero_compte = f"{prefix}-{uid}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.numero_compte} ({self.get_type_display()})"

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=(
                    models.Q(type='banque', titulaire__isnull=False) |
                    models.Q(type='operateur', titulaire__isnull=False) |
                    models.Q(type='operateur', operateur__isnull=False)
                ),

                name="compte_titulaire_ou_operateur"
            )
        ]

# ------------------------------------------------------------------
#   TRANSACTION
# ------------------------------------------------------------------
from django.db import IntegrityError
class Transaction(models.Model):
    class Statut(models.TextChoices):
        EN_ATTENTE = 'attente',   'En attente'
        TRANSMISE  = 'transmise', 'Transmise'
        ECHEC      = 'echec',     'Échec'

    reference_paiement = models.CharField(max_length=20, unique=True, editable=False)
    montant            = models.DecimalField(max_digits=15, decimal_places=2)
    date_transaction   = models.DateTimeField(auto_now_add=True)
    date_transmission  = models.DateTimeField(null=True, blank=True)
    statut             = models.CharField(max_length=10, choices=Statut.choices, default=Statut.EN_ATTENTE)

    compte_debite      = models.ForeignKey(
        Compte,
        on_delete=models.PROTECT,
        related_name='debits'
    )
    compte_credite     = models.ForeignKey(
        Compte,
        on_delete=models.PROTECT,
        related_name='credits'
    )

    valide_par         = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='transactions_validées'
    )

    nom_fichier = models.CharField(max_length=20, blank=True)

    @property
    def solde_initial_credite(self):
        if self.compte_credite and self.montant:
            return self.compte_credite.solde - self.montant
        return None
    

    def save(self, *args, **kwargs):
        if not self.reference_paiement:
            for _ in range(5):  # 5 tentatives maximum
                ref = f"TRX-{uuid.uuid4().hex[:11].upper()}"
                if not Transaction.objects.filter(reference_paiement=ref).exists():
                    self.reference_paiement = ref
                    break
            else:
                raise ValueError("Impossible de générer une référence de paiement unique.")
        
        try:
            super().save(*args, **kwargs)
        except IntegrityError:
            raise ValueError("Échec de l'enregistrement : référence de paiement déjà utilisée.")

    notification_envoyee = models.BooleanField(default=False)

    
    def __str__(self):
        return f"{self.reference_paiement} – {self.montant} ({self.get_statut_display()})"


# ------------------------------------------------------------------
#  DOCUMENT  (fichier CBS ou reçu généré)
# ------------------------------------------------------------------
def fichier_transaction_path(instance, filename):
    # Stocke sous  documents/ANNEE/MOIS/<reference>.ext
    return f"documents/{instance.date.strftime('%Y/%m')}/{instance.transaction.reference_paiement}_{filename}"

class Document(models.Model):
    libelle      = models.CharField(max_length=50)
    fichier      = models.FileField(upload_to=fichier_transaction_path)
    date         = models.DateTimeField(auto_now_add=True)
    transaction  = models.OneToOneField(
        Transaction,
        on_delete=models.CASCADE,
        related_name='document'
    )

    def __str__(self):
        return self.libelle



