from django.db import models
from datetime import date
from workspace.models import workspace # Importar el modelo workspace
from usuarios.models import usuario # Importar el modelo usuario

class tableros(models.Model):
    cod_tablero = models.AutoField(primary_key=True)
    cod_espacio = models.ForeignKey(workspace, on_delete=models.CASCADE, db_column='cod_espacio')  # Relación con el modelo workspace
    nom_tablero = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=200)
    usu_creador = models.ForeignKey(usuario, on_delete=models.CASCADE, db_column='usu_creador')  # Relación con el modelo usuario
    fec_creacion = models.DateField(auto_now_add=True)  

    class Meta:
        db_table = 'tableros'
        
class ListasTableros (models.Model):
    cod_lista = models.AutoField(primary_key=True)  # Asigna automáticamente el ID
    nom_lista = models.CharField(max_length=25)
    cant_tarjetas = models.IntegerField(default=1)
    cod_tablero = models.ForeignKey(tableros, on_delete=models.CASCADE, db_column='cod_tablero')

    class Meta:
        db_table = 'listas_tableros'
