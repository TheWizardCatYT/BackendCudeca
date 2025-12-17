from django.urls import path
from . import views

urlpatterns = [
    # Página principal
    path('', views.home, name='home'),

    # Listas de eventos
    path('cenas/', views.lista_cenas, name='lista_cenas'),
    path('rifas/', views.lista_rifas, name='lista_rifas'),
    path('marchas/', views.lista_marchas, name='lista_marchas'),
    path('conciertos/', views.lista_conciertos, name='lista_conciertos'),

    # Detalles de eventos
    path('cena/<int:pk>/', views.detalle_cena, name='detalle_cena'),
    path('rifa/<int:pk>/', views.detalle_rifa, name='detalle_rifa'),
    path('marcha/<int:pk>/', views.detalle_marcha, name='detalle_marcha'),
    path('concierto/<int:pk>/', views.detalle_concierto, name='detalle_concierto'),

    # Compra/Inscripción
    path('cena/<int:pk>/comprar/', views.comprar_entrada_cena, name='comprar_entrada_cena'),
    path('rifa/<int:pk>/comprar/', views.comprar_boleto, name='comprar_boleto'),
    path('marcha/<int:pk>/inscribir/', views.inscribir_marcha, name='inscribir_marcha'),
    path('concierto/<int:pk>/comprar/', views.comprar_entrada_concierto, name='comprar_entrada_concierto'),
]
