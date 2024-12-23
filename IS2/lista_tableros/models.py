from django.db import models
from tableros.models import tableros 

class ListaTableros (models.Model):
    cod_lista = models.AutoField(primary_key=True) 
    nom_lista = models.CharField(max_length=25)
    cant_tarjetas = models.IntegerField(default=0)
    cod_tablero = models.ForeignKey(tableros, on_delete=models.CASCADE, db_column='cod_tablero') # Relacion con el modelo tableros

    class Meta:
        db_table = 'listas_tableros'
