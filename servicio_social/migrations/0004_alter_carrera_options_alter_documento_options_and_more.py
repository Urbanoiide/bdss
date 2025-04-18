# Generated by Django 5.1.7 on 2025-04-07 01:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servicio_social', '0003_remove_documento_subido'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='carrera',
            options={'verbose_name': 'Carrera', 'verbose_name_plural': 'Carreras'},
        ),
        migrations.AlterModelOptions(
            name='documento',
            options={'verbose_name': 'Documento', 'verbose_name_plural': 'Documentos'},
        ),
        migrations.AlterModelOptions(
            name='institucion',
            options={'verbose_name': 'Institución', 'verbose_name_plural': 'Instituciones'},
        ),
        migrations.AlterModelOptions(
            name='prestador',
            options={'verbose_name': 'Prestador', 'verbose_name_plural': 'Prestadores'},
        ),
        migrations.AlterModelOptions(
            name='reporte',
            options={'verbose_name': 'Reporte', 'verbose_name_plural': 'Reportes'},
        ),
        migrations.AlterModelOptions(
            name='serviciosocial',
            options={'verbose_name': 'Servicio Social', 'verbose_name_plural': 'Servicios Sociales'},
        ),
        migrations.AlterField(
            model_name='documento',
            name='archivo',
            field=models.FileField(upload_to='reportes/'),
        ),
        migrations.CreateModel(
            name='ResumenDocumentos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('institucion', models.CharField(blank=True, max_length=100)),
                ('carta_asignacion', models.BooleanField(default=False)),
                ('reporte_parcial', models.BooleanField(default=False)),
                ('evaluacion_desempeno', models.BooleanField(default=False)),
                ('carta_termino', models.BooleanField(default=False)),
                ('prestador', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='servicio_social.prestador')),
            ],
            options={
                'verbose_name': 'Resumen de Documentos',
                'verbose_name_plural': 'Resumen de Documentos',
            },
        ),
    ]
