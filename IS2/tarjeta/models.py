from django.db import models
from lista_tableros.models import ListaTableros

class Tarjeta(models.Model):
    cod_tarjeta = models.AutoField(primary_key=True)
    nom_tarjeta = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=200)
    estado = models.CharField(max_length=3)
    usu_encargado = models.CharField(max_length=10, null=True, blank=True)
    fec_vencimiento = models.DateField(null=True, blank=True)
    cod_lista = models.ForeignKey(ListaTableros, on_delete=models.CASCADE,  db_column='cod_lista') #Relacion para tarjetas con listas
    fec_creacion = models.DateField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.pk:  # Si la tarjeta es nueva
            self.cod_lista.cant_tarjetas += 1
            self.cod_lista.save()
        super(Tarjeta, self).save(*args, **kwargs)

    class Meta:
        db_table = 'tarjetas'