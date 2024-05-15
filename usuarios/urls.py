
from django.urls import path
from . import views

urlpatterns = [
    path('', views.logar, name='logar'),
    path('logar/', views.logar, name='logar'),
    path('logout/', views.logout_view, name='logout'),
    path('cadastro_usuario/', views.cadastro, name='cadastro_usuario'),
    path('lista_usuario/', views.UserListView.as_view(), name='lista_usuario'),
]