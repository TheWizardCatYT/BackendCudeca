from django.core.validators import MinValueValidator
from django.db import models

LINK_MAX_LENGTH = 50
DESCRIPTION_MAX_LENGTH = 500
MENU_MAX_LENGTH = 1000
PREMIO_MAX_LENGTH = 200
RECORRIDO_MAX_LENGTH = 200
NAME_MAX_LENGTH = 100
# Create your models here.
# Vamos a crear una clase abstracra "evento" de la que heredarán cada tipo
class Evento(models.Model):
    fecha = models.DateTimeField()
    lugar = models.CharField(max_length=LINK_MAX_LENGTH)
    recaudacion_objetivo = models.IntegerField()
    descripcion = models.CharField(max_length=DESCRIPTION_MAX_LENGTH)
    imagen = models.ImageField()
    class Meta:
        abstract = True


# Suponiendo que se reservan las mesas en vez de asientos por separado:
class Cena(Evento):
    # La PK de cena será la heredada de evento
    menu = models.CharField(max_length=MENU_MAX_LENGTH)
    num_mesas = models.IntegerField() # Es la cantidad de mesas disponibles en el evento
    num_asientos = models.SmallIntegerField()

class Mesa(models.Model):
    num_mesa = models.BigIntegerField() #Es el número identificador de la mesa
    evento_fk = models.ForeignKey(Cena, on_delete=models.CASCADE)
    #pk = models.CompositePrimaryKey("num_mesa","evento_fk")
    asignaciones = models.SmallIntegerField()

class Rifa(Evento):
    premio = models.CharField(max_length=PREMIO_MAX_LENGTH)
    boletos_vendidos = models.IntegerField()

class Marcha(Evento):
    recorrido = models.CharField(max_length=RECORRIDO_MAX_LENGTH)

class Concierto(Evento):
    max_asistentes = models.IntegerField()
    num_filas = models.SmallIntegerField()
    num_asientos = models.IntegerField()
# TICKETS

# Y otra clase abstracta "ticket" que será la base para las entradas y tickets de cada evento
class Ticket(models.Model):
    # id = models.BigAutoField(primary_key=True) creo que esto es mejor eliminarlo
    nombre = models.CharField(max_length=NAME_MAX_LENGTH)
    usado = models.BooleanField()
    class Meta:
        abstract = True

# Ahora generamos los tickets específicos para cada evento
class EntradaCena(Ticket):
    # "Apunta" a la mesa de la cual se ha comprado la entrada
    mesa = models.ForeignKey(Mesa, on_delete=models.CASCADE)


class Boleto(Ticket):
    num = models.IntegerField() # Tu número asignado para la rifa
    rifa_fk = models.ForeignKey(Rifa, on_delete=models.CASCADE) # Puntero a la rifa en la que participas

class Dorsal(Ticket):
    TALLAS_CAMISETAS = {
        "XXS": "Extra Extra Small",
        "XS": "Extra Small",
        "S": "Small",
        "M": "Medium",
        "L": "Large",
         "XL": "Extra Large",
        "XXl": "Extra Extra Large"
    }
    num = models.IntegerField() # Numero que se te ha sido asignado como corredor
    talla = models.CharField(max_length=3, choices=TALLAS_CAMISETAS) # Talla de tu camiseta

class EntradaConcierto(Ticket):
    fila = models.SmallIntegerField() # Fila de tu asiento
    asiento = models.BigIntegerField() # El número de tu asiento