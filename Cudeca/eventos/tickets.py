import qrcode
from io import BytesIO
import base64
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse
from .models import EntradaCena, Boleto, Dorsal, EntradaConcierto


def generate_qr_code(data):
    """Generate QR code and return as base64 string"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    
    # Convert to base64 for embedding in HTML
    img_str = base64.b64encode(buffer.getvalue()).decode()
    return f"data:image/png;base64,{img_str}"


def ticket_entrada_cena(request, pk):
    """Display ticket for dinner entry"""
    entrada = get_object_or_404(EntradaCena, pk=pk)
    cena = entrada.mesa.evento_fk
    
    # Generate QR with verification URL
    verification_url = request.build_absolute_uri(
        reverse('verificar_ticket_cena', kwargs={'pk': pk})
    )
    qr_code = generate_qr_code(verification_url)
    
    context = {
        'entrada': entrada,
        'cena': cena,
        'qr_code': qr_code,
        'tipo': 'Entrada de Cena',
    }
    return render(request, 'eventos/ticket_cena.html', context)


def ticket_boleto(request, pk):
    """Display ticket for raffle"""
    boleto = get_object_or_404(Boleto, pk=pk)
    rifa = boleto.rifa_fk
    
    verification_url = request.build_absolute_uri(
        reverse('verificar_ticket_boleto', kwargs={'pk': pk})
    )
    qr_code = generate_qr_code(verification_url)
    
    context = {
        'boleto': boleto,
        'rifa': rifa,
        'qr_code': qr_code,
        'tipo': 'Boleto de Rifa',
    }
    return render(request, 'eventos/ticket_boleto.html', context)


def ticket_dorsal(request, pk):
    """Display ticket for race bib"""
    dorsal = get_object_or_404(Dorsal, pk=pk)
    marcha = dorsal.marcha_fk
    
    verification_url = request.build_absolute_uri(
        reverse('verificar_ticket_dorsal', kwargs={'pk': pk})
    )
    qr_code = generate_qr_code(verification_url)
    
    context = {
        'dorsal': dorsal,
        'marcha': marcha,
        'qr_code': qr_code,
        'tipo': 'Dorsal de Marcha',
    }
    return render(request, 'eventos/ticket_dorsal.html', context)


def ticket_concierto(request, pk):
    """Display ticket for concert"""
    entrada = get_object_or_404(EntradaConcierto, pk=pk)
    concierto = entrada.concierto_fk
    
    verification_url = request.build_absolute_uri(
        reverse('verificar_ticket_concierto', kwargs={'pk': pk})
    )
    qr_code = generate_qr_code(verification_url)
    
    context = {
        'entrada': entrada,
        'concierto': concierto,
        'qr_code': qr_code,
        'tipo': 'Entrada de Concierto',
    }
    return render(request, 'eventos/ticket_concierto.html', context)


# Verification views
def verificar_ticket_cena(request, pk):
    """Verify and mark dinner ticket as used"""
    entrada = get_object_or_404(EntradaCena, pk=pk)
    cena = entrada.mesa.evento_fk
    
    if request.method == 'POST':
        entrada.usado = True
        entrada.save()
        return render(request, 'eventos/verificacion_exitosa.html', {
            'ticket': entrada,
            'evento': cena,
            'tipo': 'Entrada de Cena'
        })
    
    context = {
        'entrada': entrada,
        'cena': cena,
        'tipo': 'Entrada de Cena',
    }
    return render(request, 'eventos/verificar_ticket.html', context)


def verificar_ticket_boleto(request, pk):
    """Verify raffle ticket"""
    boleto = get_object_or_404(Boleto, pk=pk)
    rifa = boleto.rifa_fk
    
    if request.method == 'POST':
        boleto.usado = True
        boleto.save()
        return render(request, 'eventos/verificacion_exitosa.html', {
            'ticket': boleto,
            'evento': rifa,
            'tipo': 'Boleto de Rifa'
        })
    
    context = {
        'boleto': boleto,
        'rifa': rifa,
        'tipo': 'Boleto de Rifa',
    }
    return render(request, 'eventos/verificar_ticket.html', context)


def verificar_ticket_dorsal(request, pk):
    """Verify race bib"""
    dorsal = get_object_or_404(Dorsal, pk=pk)
    marcha = dorsal.marcha_fk
    
    if request.method == 'POST':
        dorsal.usado = True
        dorsal.save()
        return render(request, 'eventos/verificacion_exitosa.html', {
            'ticket': dorsal,
            'evento': marcha,
            'tipo': 'Dorsal de Marcha'
        })
    
    context = {
        'dorsal': dorsal,
        'marcha': marcha,
        'tipo': 'Dorsal de Marcha',
    }
    return render(request, 'eventos/verificar_ticket.html', context)


def verificar_ticket_concierto(request, pk):
    """Verify concert ticket"""
    entrada = get_object_or_404(EntradaConcierto, pk=pk)
    concierto = entrada.concierto_fk
    
    if request.method == 'POST':
        entrada.usado = True
        entrada.save()
        return render(request, 'eventos/verificacion_exitosa.html', {
            'ticket': entrada,
            'evento': concierto,
            'tipo': 'Entrada de Concierto'
        })
    
    context = {
        'entrada': entrada,
        'concierto': concierto,
        'tipo': 'Entrada de Concierto',
    }
    return render(request, 'eventos/verificar_ticket.html', context)
