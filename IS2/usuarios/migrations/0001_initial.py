# Generated by Django 5.1.1 on 2024-10-08 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='usuario',
            fields=[
                ('cod_usuario', models.AutoField(primary_key=True, serialize=False)),
                ('nom_usuario', models.CharField(max_length=255)),
                ('dir_correo', models.CharField(max_length=255)),
                ('pass_usuario', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'usuarios',
            },
        ),
    ]
