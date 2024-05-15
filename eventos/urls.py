
from django.urls import path
from . import views


urlpatterns = [
    path('cadastro_evento/', views.cadastro_evento, name='cadastro_evento'),
    path('eventos_criar/', views.AgendarEventosCreateView.as_view(), name ='eventos_criar'),
    path('listar_eventos/', views.AgendarEventosListView.as_view(), name='listar_eventos'),
    path('atualizar_evento/', views.AtualizarEvento.as_view(), name='atualizar_evento'),
    path('compartilhar/', views.CompartilharEventosListView.as_view(), name='compartilhar_eventos'),
    path('evento_detalhe/<int:pk>', views.AgendarEventosDetailView.as_view(), name ='evento_detalhe'),
    path('artistas_list/', views.artistas_list, name='artistas_list'),
    path('alterar_artista/<int:id>/', views.alterar_artista, name='alterar_artista'),
    path('adicionar_artista/', views.adicionar_artista, name='adicionar_artista'),
    path('deletar_artista/', views.deletar_artista, name='deletar_artista'),
    path('origem_destino/', views.origem_destino, name='origem_destino'),
    path('nova_parcela/', views.nova_parcela, name='nova_parcela'),
    path('remover_pagamento/', views.remover_pagamento, name='remover_pagamento'),
    path('remover_evento/', views.remover_evento, name='remover_evento'),
]