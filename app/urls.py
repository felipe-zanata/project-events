
from django.contrib import admin
from django.urls import path, include
from eventos import views

urlpatterns = [
    path('', include('usuarios.urls')),
    path('admin/', admin.site.urls),
    path('eventos/', include('eventos.urls')),
    path('usuarios/', include('usuarios.urls')),
    path('obter_cidades/', views.obter_cidades, name='obter_cidades'),
    path('obter_uf_cidades/', views.ObterUFCidadesView.as_view(), name ='obter_uf_cidades'),
]
