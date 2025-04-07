from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class Carrera(models.Model):
    nombre = models.CharField(max_length=100)
    class Meta:
        verbose_name = "Carrera"
        verbose_name_plural = "Carreras"   
    def __str__(self):
        return self.nombre 


class Prestador(models.Model):
    nombres = models.CharField(max_length=50)
    apellido_p = models.CharField(max_length=50)
    apellido_m = models.CharField(max_length=50)
    curp = models.CharField(max_length=50, unique=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    correo = models.EmailField(unique=True)
    matricula = models.CharField(max_length=50, unique=True)
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE)
    activo = models.BooleanField(default=True)
    class Meta:
        verbose_name = "Prestador"
        verbose_name_plural = "Prestadores"
    def __str__(self):
        return f"{self.matricula} - {'Activo' if self.activo else 'Inactivo'}"


class Institucion(models.Model):
    nombre = models.CharField(max_length=100)
    class Meta:
        verbose_name = "Institución"
        verbose_name_plural = "Instituciones"
    def __str__(self):
        return self.nombre


class ServicioSocial(models.Model):
    prestador = models.ForeignKey(Prestador, on_delete=models.CASCADE)
    institucion = models.ForeignKey(Institucion, on_delete=models.CASCADE)
    programa = models.CharField(max_length=100)
    responsable = models.CharField(max_length=100)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    horas_requeridas = models.IntegerField(default=480)
    horas_realizadas = models.IntegerField(default=0)
    actividades = models.TextField()
    class Meta:
        verbose_name = "Servicio Social"
        verbose_name_plural = "Servicios Sociales"
    def __str__(self):
        return f"{self.prestador.matricula} - {self.institucion.nombre}"


class Documento(models.Model):
    TIPOS = [
        ('Carta de asignación', 'Carta de asignación'),
        ('Reporte parcial', 'Reporte parcial'),
        ('Evaluación de desempeño', 'Evaluación de desempeño'),
        ('Carta de término', 'Carta de término'),
    ]
    prestador = models.ForeignKey(Prestador, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=50, choices=TIPOS)
    archivo = models.FileField(upload_to='reportes/')
    class Meta:
        verbose_name = "Documento"
        verbose_name_plural = "Documentos"
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Guarda el documento primero

        # Si el tipo es "Carta de término", marcar al prestador como inactivo
        if self.tipo == 'Carta de término':
            self.prestador.activo = False
            self.prestador.save()  # Guardar el cambio en la base de datos
    def __str__(self):
        return self.tipo + " - " + self.prestador.matricula


class Reporte(models.Model):
    servicio = models.ForeignKey(ServicioSocial, on_delete=models.CASCADE)
    numero_reporte = models.IntegerField()
    archivo = models.FileField(upload_to='reportes/')
    fecha_subida = models.DateField(auto_now_add=True)
    class Meta:
        verbose_name = "Reporte"
        verbose_name_plural = "Reportes"
    def __str__(self):
        return self.servicio.prestador.matricula + ",Reporte numero: " + str(self.numero_reporte)


# NUEVO MODELO: ResumenDocumentos

class ResumenDocumentos(models.Model):
    servicio_social = models.ForeignKey(ServicioSocial, on_delete=models.CASCADE, default=1)  # Use a valid ID from ServicioSocial
    carta_asignacion = models.BooleanField(default=False)
    reporte_parcial = models.BooleanField(default=False)
    evaluacion_desempeno = models.BooleanField(default=False)
    carta_termino = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Resumen de Documentos"
        verbose_name_plural = "Resumen de Documentos"

    def __str__(self):
        return f"{self.servicio_social.prestador.matricula} - {self.servicio_social.institucion.nombre} - Resumen de Documentos"



# SEÑAL AUTOMÁTICA

@receiver(post_save, sender=Documento)
def actualizar_resumen_documentos(sender, instance, **kwargs):
    tipos = {
        'Carta de asignación': 'carta_asignacion',
        'Reporte parcial': 'reporte_parcial',
        'Evaluación de desempeño': 'evaluacion_desempeno',
        'Carta de término': 'carta_termino',
    }

    prestador = instance.prestador
    servicio = ServicioSocial.objects.filter(prestador=prestador).first()
    
    if servicio:
        resumen, _ = ResumenDocumentos.objects.get_or_create(servicio_social=servicio)

        # Verificar qué documentos tiene el prestador
        documentos = Documento.objects.filter(prestador=prestador).values_list('tipo', flat=True)

        for tipo_doc, campo in tipos.items():
            setattr(resumen, campo, tipo_doc in documentos)

        resumen.save()

