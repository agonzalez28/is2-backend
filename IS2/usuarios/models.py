from django.db import models

class usuario(models.Model):
    cod_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    nom_usuario = models.CharField(max_length=255, unique = True)
    dir_correo = models.CharField(max_length=255, unique = True)
    pass_usuario = models.CharField(max_length=255)

    class Meta:
        db_table = 'usuarios'

