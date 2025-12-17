from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone

LINK_MAX_LENGTH = 50
DESCRIPTION_MAX_LENGTH = 500
MENU_MAX_LENGTH = 1000
PREMIO_MAX_LENGTH = 200
RECORRIDO_MAX_LENGTH = 200
NAME_MAX_LENGTH = 100


class Evento(models.Model):
    fecha = models.DateTimeField(default=timezone.now)
    lugar = models.CharField(max_length=LINK_MAX_LENGTH)
    recaudacion_objetivo = models.IntegerField(validators=[MinValueValidator(0)])
    recaudacion_actual = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    descripcion = models.CharField(max_length=DESCRIPTION_MAX_LENGTH)
    imagen = models.ImageField(upload_to='eventos/', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True
        ordering = ['-fecha']

    def porcentaje_recaudado(self):
        if self.recaudacion_objetivo > 0:
            return (self.recaudacion_actual / self.recaudacion_objetivo) * 100
        return 0


class Cena(Evento):
    menu = models.CharField(max_length=MENU_MAX_LENGTH)
    num_mesas = models.IntegerField(validators=[MinValueValidator(1)])
    num_asientos = models.SmallIntegerField(validators=[MinValueValidator(1)])
    precio_por_persona = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)],
                                             default=0)

    def __str__(self):
        return f"Cena - {self.lugar} ({self.fecha.strftime('%d/%m/%Y')})"

    class Meta:
        verbose_name = "Cena"
        verbose_name_plural = "Cenas"


class Mesa(models.Model):
    num_mesa = models.IntegerField(validators=[MinValueValidator(1)])
    evento_fk = models.ForeignKey(Cena, on_delete=models.CASCADE, related_name='mesas')
    asignaciones = models.SmallIntegerField(default=0, validators=[MinValueValidator(0)])

    class Meta:
        unique_together = ('num_mesa', 'evento_fk')
        ordering = ['num_mesa']

    def __str__(self):
        return f"Mesa {self.num_mesa} - {self.evento_fk.lugar}"

    def asientos_disponibles(self):
        return self.evento_fk.num_asientos - self.asignaciones


class Rifa(Evento):
    premio = models.CharField(max_length=PREMIO_MAX_LENGTH)
    boletos_vendidos = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    precio_boleto = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], default=0)
    max_boletos = models.IntegerField(validators=[MinValueValidator(1)], default=100)

    def __str__(self):
        return f"Rifa - {self.premio} ({self.fecha.strftime('%d/%m/%Y')})"

    class Meta:
        verbose_name = "Rifa"
        verbose_name_plural = "Rifas"


class Marcha(Evento):
    recorrido = models.CharField(max_length=RECORRIDO_MAX_LENGTH)
    precio_inscripcion = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)],
                                             default=0)
    max_participantes = models.IntegerField(validators=[MinValueValidator(1)], default=100)

    def __str__(self):
        return f"Marcha - {self.lugar} ({self.fecha.strftime('%d/%m/%Y')})"

    class Meta:
        verbose_name = "Marcha"
        verbose_name_plural = "Marchas"


class Concierto(Evento):
    max_asistentes = models.IntegerField(validators=[MinValueValidator(1)])
    num_filas = models.SmallIntegerField(validators=[MinValueValidator(1)])
    num_asientos = models.IntegerField(validators=[MinValueValidator(1)])
    precio_entrada = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], default=0)

    def __str__(self):
        return f"Concierto - {self.lugar} ({self.fecha.strftime('%d/%m/%Y')})"

    class Meta:
        verbose_name = "Concierto"
        verbose_name_plural = "Conciertos"


class Ticket(models.Model):
    nombre = models.CharField(max_length=NAME_MAX_LENGTH)
    email = models.EmailField(blank=True, default='')
    telefono = models.CharField(max_length=20, blank=True, default='')
    usado = models.BooleanField(default=False)
    fecha_compra = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True


class EntradaCena(Ticket):
    mesa = models.ForeignKey(Mesa, on_delete=models.CASCADE, related_name='entradas')

    def __str__(self):
        return f"Entrada Cena - {self.nombre} - Mesa {self.mesa.num_mesa}"

    class Meta:
        verbose_name = "Entrada de Cena"
        verbose_name_plural = "Entradas de Cena"


class Boleto(Ticket):
    num = models.IntegerField(validators=[MinValueValidator(1)])
    rifa_fk = models.ForeignKey(Rifa, on_delete=models.CASCADE, related_name='boletos')

    class Meta:
        unique_together = ('num', 'rifa_fk')
        ordering = ['num']
        verbose_name = "Boleto de Rifa"
        verbose_name_plural = "Boletos de Rifa"

    def __str__(self):
        return f"Boleto #{self.num} - {self.nombre} - {self.rifa_fk.premio}"


class Dorsal(Ticket):
    TALLAS_CAMISETAS = {
        "XXS": "Extra Extra Small",
        "XS": "Extra Small",
        "S": "Small",
        "M": "Medium",
        "L": "Large",
        "XL": "Extra Large",
        "XXL": "Extra Extra Large"
    }
    num = models.IntegerField(validators=[MinValueValidator(1)])
    talla = models.CharField(max_length=3, choices=TALLAS_CAMISETAS)
    marcha_fk = models.ForeignKey(Marcha, on_delete=models.CASCADE, related_name='dorsales')

    class Meta:
        unique_together = ('num', 'marcha_fk')
        ordering = ['num']
        verbose_name = "Dorsal de Marcha"
        verbose_name_plural = "Dorsales de Marcha"

    def __str__(self):
        return f"Dorsal #{self.num} - {self.nombre}"


class EntradaConcierto(Ticket):
    fila = models.SmallIntegerField(validators=[MinValueValidator(1)])
    asiento = models.IntegerField(validators=[MinValueValidator(1)])
    concierto_fk = models.ForeignKey(Concierto, on_delete=models.CASCADE, related_name='entradas')

    class Meta:
        unique_together = ('fila', 'asiento', 'concierto_fk')
        ordering = ['fila', 'asiento']
        verbose_name = "Entrada de Concierto"
        verbose_name_plural = "Entradas de Concierto"

    def __str__(self):
        return f"Entrada Concierto - {self.nombre} - Fila {self.fila}, Asiento {self.asiento}"