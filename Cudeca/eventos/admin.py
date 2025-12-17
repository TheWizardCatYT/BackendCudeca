from django.contrib import admin
from .models import (
    Cena, Mesa, Rifa, Marcha, Concierto,
    EntradaCena, Boleto, Dorsal, EntradaConcierto
)


class MesaInline(admin.TabularInline):
    model = Mesa
    extra = 1
    fields = ('num_mesa', 'asignaciones')


@admin.register(Cena)
class CenaAdmin(admin.ModelAdmin):
    list_display = ('lugar', 'fecha', 'num_mesas', 'precio_por_persona', 'recaudacion_actual', 'recaudacion_objetivo')
    list_filter = ('fecha',)
    search_fields = ('lugar', 'descripcion')
    inlines = [MesaInline]
    fieldsets = (
        ('Información General', {
            'fields': ('fecha', 'lugar', 'descripcion', 'imagen')
        }),
        ('Detalles de Cena', {
            'fields': ('menu', 'num_mesas', 'num_asientos', 'precio_por_persona')
        }),
        ('Recaudación', {
            'fields': ('recaudacion_objetivo', 'recaudacion_actual')
        }),
    )


@admin.register(Mesa)
class MesaAdmin(admin.ModelAdmin):
    list_display = ('num_mesa', 'evento_fk', 'asignaciones', 'asientos_disponibles')
    list_filter = ('evento_fk',)
    search_fields = ('num_mesa',)


@admin.register(Rifa)
class RifaAdmin(admin.ModelAdmin):
    list_display = ('premio', 'fecha', 'precio_boleto', 'boletos_vendidos', 'max_boletos', 'recaudacion_actual', 'recaudacion_objetivo')
    list_filter = ('fecha',)
    search_fields = ('premio', 'descripcion')
    fieldsets = (
        ('Información General', {
            'fields': ('fecha', 'lugar', 'descripcion', 'imagen')
        }),
        ('Detalles de Rifa', {
            'fields': ('premio', 'precio_boleto', 'max_boletos', 'boletos_vendidos')
        }),
        ('Recaudación', {
            'fields': ('recaudacion_objetivo', 'recaudacion_actual')
        }),
    )


@admin.register(Marcha)
class MarchaAdmin(admin.ModelAdmin):
    list_display = ('lugar', 'fecha', 'precio_inscripcion', 'max_participantes', 'recaudacion_actual', 'recaudacion_objetivo')
    list_filter = ('fecha',)
    search_fields = ('lugar', 'recorrido', 'descripcion')
    fieldsets = (
        ('Información General', {
            'fields': ('fecha', 'lugar', 'descripcion', 'imagen')
        }),
        ('Detalles de Marcha', {
            'fields': ('recorrido', 'precio_inscripcion', 'max_participantes')
        }),
        ('Recaudación', {
            'fields': ('recaudacion_objetivo', 'recaudacion_actual')
        }),
    )


@admin.register(Concierto)
class ConciertoAdmin(admin.ModelAdmin):
    list_display = ('lugar', 'fecha', 'max_asistentes', 'precio_entrada', 'recaudacion_actual', 'recaudacion_objetivo')
    list_filter = ('fecha',)
    search_fields = ('lugar', 'descripcion')
    fieldsets = (
        ('Información General', {
            'fields': ('fecha', 'lugar', 'descripcion', 'imagen')
        }),
        ('Detalles de Concierto', {
            'fields': ('max_asistentes', 'num_filas', 'num_asientos', 'precio_entrada')
        }),
        ('Recaudación', {
            'fields': ('recaudacion_objetivo', 'recaudacion_actual')
        }),
    )


@admin.register(EntradaCena)
class EntradaCenaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'mesa', 'usado', 'fecha_compra')
    list_filter = ('usado', 'fecha_compra', 'mesa__evento_fk')
    search_fields = ('nombre', 'email')


@admin.register(Boleto)
class BoletoAdmin(admin.ModelAdmin):
    list_display = ('num', 'nombre', 'email', 'rifa_fk', 'usado', 'fecha_compra')
    list_filter = ('usado', 'fecha_compra', 'rifa_fk')
    search_fields = ('nombre', 'email', 'num')


@admin.register(Dorsal)
class DorsalAdmin(admin.ModelAdmin):
    list_display = ('num', 'nombre', 'email', 'talla', 'marcha_fk', 'usado', 'fecha_compra')
    list_filter = ('usado', 'talla', 'fecha_compra', 'marcha_fk')
    search_fields = ('nombre', 'email', 'num')


@admin.register(EntradaConcierto)
class EntradaConciertoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'fila', 'asiento', 'concierto_fk', 'usado', 'fecha_compra')
    list_filter = ('usado', 'fecha_compra', 'concierto_fk')
    search_fields = ('nombre', 'email')