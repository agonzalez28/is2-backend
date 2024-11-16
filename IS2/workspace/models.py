from django.db import models
from datetime import date 
from usuarios.models import usuario # Importar el modelo usuario

class workspace(models.Model):
    cod_espacio = models.AutoField(primary_key=True)
    nom_proyecto = models.CharField(max_length=255)
    descripcion = models.CharField(max_length=255)
    estado = models.CharField(max_length=50)
    usu_creador = models.ForeignKey(usuario, on_delete=models.CASCADE, db_column='usu_creador') # Relación con el modelo usuario 
    fec_creacion = models.DateField(default=date.today)
    usu_modificacion = models.CharField(max_length=255)
    fec_modificacion = models.DateField(auto_now=True)
    usuarios = models.ManyToManyField(usuario, related_name='workspaces', blank=True) #Relacion para usuarios asignados en el workspace

    class Meta:
        db_table = 'espacios'

