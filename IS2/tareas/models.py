from django.db import models
from tarjeta.models import Tarjeta  # Tarea está relacionada con Tarjetas

class Tarea(models.Model):
    cod_tarea = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=200) 
    estado = models.CharField(max_length=50)  
    cod_tarjeta = models.ForeignKey(Tarjeta, on_delete=models.CASCADE, db_column='cod_tarjeta')  # Relación con Tarjeta 
    fec_creacion = models.DateField(auto_now_add=True) 
    fec_vencimiento = models.DateField() 

    class Meta:
        db_table = 'tareas'
