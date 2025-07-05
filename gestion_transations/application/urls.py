from django.urls import path
from . import views
from django.contrib.auth.views import LoginView
from application.forms import CustomLoginForm


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

    
    


]