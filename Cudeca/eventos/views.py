from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from .models import Cena, Rifa, Marcha, Concierto, Mesa, EntradaCena, Boleto, Dorsal, EntradaConcierto


def home(request):
    """Vista principal con todos los eventos próximos"""
    now = timezone.now()

    cenas = Cena.objects.filter(fecha__gte=now)[:3]
    rifas = Rifa.objects.filter(fecha__gte=now)[:3]
    marchas = Marcha.objects.filter(fecha__gte=now)[:3]
    conciertos = Concierto.objects.filter(fecha__gte=now)[:3]

    context = {
        'cenas': cenas,
        'rifas': rifas,
        'marchas': marchas,
        'conciertos': conciertos,
    }
    return render(request, 'eventos/home.html', context)


# VISTAS DE LISTADO
def lista_cenas(request):
    cenas = Cena.objects.filter(fecha__gte=timezone.now())
    return render(request, 'eventos/lista_cenas.html', {'cenas': cenas})


def lista_rifas(request):
    rifas = Rifa.objects.filter(fecha__gte=timezone.now())
    return render(request, 'eventos/lista_rifas.html', {'rifas': rifas})


def lista_marchas(request):
    marchas = Marcha.objects.filter(fecha__gte=timezone.now())
    return render(request, 'eventos/lista_marchas.html', {'marchas': marchas})


def lista_conciertos(request):
    conciertos = Concierto.objects.filter(fecha__gte=timezone.now())
    return render(request, 'eventos/lista_conciertos.html', {'conciertos': conciertos})


# VISTAS DE DETALLE
def detalle_cena(request, pk):
    cena = get_object_or_404(Cena, pk=pk)
    mesas = cena.mesas.all()
    context = {
        'cena': cena,
        'mesas': mesas,
    }
    return render(request, 'eventos/detalle_cena.html', context)


def detalle_rifa(request, pk):
    rifa = get_object_or_404(Rifa, pk=pk)
    boletos_disponibles = rifa.max_boletos - rifa.boletos_vendidos
    context = {
        'rifa': rifa,
        'boletos_disponibles': boletos_disponibles,
    }
    return render(request, 'eventos/detalle_rifa.html', context)


def detalle_marcha(request, pk):
    marcha = get_object_or_404(Marcha, pk=pk)
    dorsales_vendidos = marcha.dorsales.count()
    plazas_disponibles = marcha.max_participantes - dorsales_vendidos
    context = {
        'marcha': marcha,
        'plazas_disponibles': plazas_disponibles,
    }
    return render(request, 'eventos/detalle_marcha.html', context)


def detalle_concierto(request, pk):
    concierto = get_object_or_404(Concierto, pk=pk)
    entradas_vendidas = concierto.entradas.count()
    entradas_disponibles = concierto.max_asistentes - entradas_vendidas
    context = {
        'concierto': concierto,
        'entradas_disponibles': entradas_disponibles,
    }
    return render(request, 'eventos/detalle_concierto.html', context)


# VISTAS DE COMPRA/INSCRIPCIÓN
def comprar_entrada_cena(request, pk):
    cena = get_object_or_404(Cena, pk=pk)

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        telefono = request.POST.get('telefono', '')
        mesa_id = request.POST.get('mesa')

        mesa = get_object_or_404(Mesa, pk=mesa_id)

        if mesa.asientos_disponibles() > 0:
            entrada = EntradaCena.objects.create(
                nombre=nombre,
                email=email,
                telefono=telefono,
                mesa=mesa
            )
            mesa.asignaciones += 1
            mesa.save()

            cena.recaudacion_actual += float(cena.precio_por_persona)
            cena.save()

            messages.success(request, f'¡Entrada comprada con éxito! Mesa {mesa.num_mesa}')
            return redirect('detalle_cena', pk=pk)
        else:
            messages.error(request, 'No hay asientos disponibles en esta mesa.')

    mesas_disponibles = [m for m in cena.mesas.all() if m.asientos_disponibles() > 0]
    context = {
        'cena': cena,
        'mesas_disponibles': mesas_disponibles,
    }
    return render(request, 'eventos/comprar_entrada_cena.html', context)


def comprar_boleto(request, pk):
    rifa = get_object_or_404(Rifa, pk=pk)

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        telefono = request.POST.get('telefono', '')

        if rifa.boletos_vendidos < rifa.max_boletos:
            # Generar número de boleto
            ultimo_boleto = rifa.boletos.order_by('-num').first()
            nuevo_num = ultimo_boleto.num + 1 if ultimo_boleto else 1

            boleto = Boleto.objects.create(
                nombre=nombre,
                email=email,
                telefono=telefono,
                num=nuevo_num,
                rifa_fk=rifa
            )

            rifa.boletos_vendidos += 1
            rifa.recaudacion_actual += float(rifa.precio_boleto)
            rifa.save()

            messages.success(request, f'¡Boleto #{nuevo_num} comprado con éxito!')
            return redirect('detalle_rifa', pk=pk)
        else:
            messages.error(request, 'No hay boletos disponibles.')

    context = {'rifa': rifa}
    return render(request, 'eventos/comprar_boleto.html', context)


def inscribir_marcha(request, pk):
    marcha = get_object_or_404(Marcha, pk=pk)

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        telefono = request.POST.get('telefono', '')
        talla = request.POST.get('talla')

        dorsales_vendidos = marcha.dorsales.count()

        if dorsales_vendidos < marcha.max_participantes:
            # Generar número de dorsal
            ultimo_dorsal = marcha.dorsales.order_by('-num').first()
            nuevo_num = ultimo_dorsal.num + 1 if ultimo_dorsal else 1

            dorsal = Dorsal.objects.create(
                nombre=nombre,
                email=email,
                telefono=telefono,
                num=nuevo_num,
                talla=talla,
                marcha_fk=marcha
            )

            marcha.recaudacion_actual += float(marcha.precio_inscripcion)
            marcha.save()

            messages.success(request, f'¡Inscripción exitosa! Dorsal #{nuevo_num}')
            return redirect('detalle_marcha', pk=pk)
        else:
            messages.error(request, 'No hay plazas disponibles.')

    context = {
        'marcha': marcha,
        'tallas': Dorsal.TALLAS_CAMISETAS,
    }
    return render(request, 'eventos/inscribir_marcha.html', context)


def comprar_entrada_concierto(request, pk):
    concierto = get_object_or_404(Concierto, pk=pk)

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        telefono = request.POST.get('telefono', '')
        fila = request.POST.get('fila')
        asiento = request.POST.get('asiento')

        # Verificar si el asiento está disponible
        existe = EntradaConcierto.objects.filter(
            concierto_fk=concierto,
            fila=fila,
            asiento=asiento
        ).exists()

        if not existe:
            entrada = EntradaConcierto.objects.create(
                nombre=nombre,
                email=email,
                telefono=telefono,
                fila=fila,
                asiento=asiento,
                concierto_fk=concierto
            )

            concierto.recaudacion_actual += float(concierto.precio_entrada)
            concierto.save()

            messages.success(request, f'¡Entrada comprada! Fila {fila}, Asiento {asiento}')
            return redirect('detalle_concierto', pk=pk)
        else:
            messages.error(request, 'Este asiento ya está ocupado.')

    # Obtener asientos ocupados para mostrar en el template
    asientos_ocupados = list(concierto.entradas.values_list('fila', 'asiento'))
    context = {
        'concierto': concierto,
        'asientos_ocupados': asientos_ocupados,
    }
    return render(request, 'eventos/comprar_entrada_concierto.html', context)