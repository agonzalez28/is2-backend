# Generated by Django 5.1.2 on 2024-11-02 00:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0004_alter_usuario_dir_correo_alter_usuario_nom_usuario'),
        ('workspace', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='workspace',
            name='usuarios',
            field=models.ManyToManyField(blank=True, related_name='workspaces', to='usuarios.usuario'),
        ),
    ]
