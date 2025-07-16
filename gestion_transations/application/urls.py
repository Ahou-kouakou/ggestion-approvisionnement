from django.urls import path
from . import views
from django.contrib.auth.views import LoginView
from application.forms import CustomLoginForm
from django.contrib.auth import views as auth_views
from django.urls import path
#from .views import redirect_after_login


urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    #path('creer-compte-client/', views.creer_compte_client_view, name='creer_compte_client'),  # à créer
    path('', LoginView.as_view(
        template_name='registration/login.html',
        authentication_form=CustomLoginForm
    ), name='login'),

    path('comptes/nouveau/', views.creer_compte_view, name='creer_compte'),
    path('compte/recharger/', views.recharger_compte_view, name='recharger_compte'),
    path('compte/operateur/nouveau/', views.creer_compte_operateur, name='creer_compte_operateur'),
    path('logout/', views.logout_view, name='logout'),
    path('transaction/creer/', views.creer_transaction, name='transaction_form'),
    path('transaction/recu/<int:transaction_id>/', views.recu_transaction, name='recu_transaction'),
    path('transaction/<int:transaction_id>/retransmettre/', views.retransmettre_transaction, name='retransmettre_transaction'),

    path('api/transactions/', views.api_transactions, name='api_transactions'),
    
    # path('connexion/', auth_views.LoginView.as_view(template_name='connexion.html'), name='connexion'),
    # path('deconnexion/', auth_views.LogoutView.as_view(), name='deconnexion'),
    # path('client/dashboard/', views.dashboard_client, name='dashboard_client'),
    #path('redirect/', redirect_after_login, name='redirect_after_login'),
    path('mes-comptes/', views.mes_comptes_view, name='mes_comptes'),

    path('utilisateur/client_operateur/creer/', views.creer_client_operateur, name='creer_client_operateur'),
    path('client/dashboard/', views.espace_client_operateur, name='client_dashboard'),
    path('transaction/creer/', views.creer_transaction, name='creer_transaction'),
        path('api/retransmettre/<int:id>/', views.retransmettre_transaction, name='retransmettre_transaction'),
]