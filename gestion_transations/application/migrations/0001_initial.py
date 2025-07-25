# Generated by Django 5.2.1 on 2025-06-28 17:21

import application.models
import django.contrib.auth.models
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Operateur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=50, unique=True)),
                ('type', models.CharField(max_length=50)),
                ('adresse', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=150, unique=True, verbose_name='Adresse Email')),
                ('telephone', models.CharField(max_length=10, validators=[django.core.validators.RegexValidator('^\\d{10}$', 'Entrez un numéro de téléphone valide à 10 chiffres.')], verbose_name='Téléphone')),
                ('user_type', models.CharField(choices=[('client', 'Client'), ('agent', 'Agent'), ('admin', 'Administrateur')], default='client', max_length=10, verbose_name="Type d'utilisateur")),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Compte',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_compte', models.CharField(blank=True, max_length=30, unique=True)),
                ('solde', models.DecimalField(decimal_places=2, default=0, max_digits=15)),
                ('type', models.CharField(choices=[('banque', 'Banque'), ('operateur', 'Opérateur')], max_length=10)),
                ('titulaire', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comptes', to=settings.AUTH_USER_MODEL)),
                ('operateur', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comptes', to='application.operateur')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference_paiement', models.CharField(editable=False, max_length=15, unique=True)),
                ('montant', models.DecimalField(decimal_places=2, max_digits=15)),
                ('date_transaction', models.DateTimeField(auto_now_add=True)),
                ('date_transmission', models.DateTimeField(blank=True, null=True)),
                ('statut', models.CharField(choices=[('attente', 'En attente'), ('transmise', 'Transmise'), ('echec', 'Échec')], default='attente', max_length=10)),
                ('nom_fichier', models.CharField(blank=True, max_length=20)),
                ('compte_credite', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='credits', to='application.compte')),
                ('compte_debite', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='debits', to='application.compte')),
                ('valide_par', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='transactions_validées', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('libelle', models.CharField(max_length=50)),
                ('fichier', models.FileField(upload_to=application.models.fichier_transaction_path)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('transaction', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='document', to='application.transaction')),
            ],
        ),
        migrations.AddConstraint(
            model_name='compte',
            constraint=models.CheckConstraint(condition=models.Q(models.Q(('operateur__isnull', True), ('titulaire__isnull', False), ('type', 'banque')), models.Q(('operateur__isnull', False), ('titulaire__isnull', True), ('type', 'operateur')), _connector='OR'), name='compte_titulaire_ou_operateur'),
        ),
    ]
