# Generated by Django 5.1.7 on 2025-03-30 02:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('servicio_social', '0002_prestador_activo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='documento',
            name='subido',
        ),
    ]
