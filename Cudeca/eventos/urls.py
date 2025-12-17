from django.urls import path
from . import views
from . import tickets

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

    # ========== NEW SECTION BELOW ==========

    # Tickets (visualización)
    path('ticket/cena/<int:pk>/', tickets.ticket_entrada_cena, name='ticket_entrada_cena'),
    path('ticket/boleto/<int:pk>/', tickets.ticket_boleto, name='ticket_boleto'),
    path('ticket/dorsal/<int:pk>/', tickets.ticket_dorsal, name='ticket_dorsal'),
    path('ticket/concierto/<int:pk>/', tickets.ticket_concierto, name='ticket_concierto'),

    # Verificación de tickets
    path('verificar/cena/<int:pk>/', tickets.verificar_ticket_cena, name='verificar_ticket_cena'),
    path('verificar/boleto/<int:pk>/', tickets.verificar_ticket_boleto, name='verificar_ticket_boleto'),
    path('verificar/dorsal/<int:pk>/', tickets.verificar_ticket_dorsal, name='verificar_ticket_dorsal'),
    path('verificar/concierto/<int:pk>/', tickets.verificar_ticket_concierto, name='verificar_ticket_concierto'),
]