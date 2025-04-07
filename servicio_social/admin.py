from django.contrib import admin

from django.contrib import admin
from .models import Carrera, Prestador, Institucion, ServicioSocial, Documento, Reporte, ResumenDocumentos

admin.site.register(Carrera)
admin.site.register(Prestador)
admin.site.register(Institucion)
admin.site.register(ServicioSocial)
admin.site.register(Documento)
admin.site.register(Reporte)

class ResumenDocumentosAdmin(admin.ModelAdmin):
    # En list_display, accedemos a los campos de servicio_social
    list_display = ('prestador', 'institucion', 'carta_asignacion', 'reporte_parcial', 'evaluacion_desempeno', 'carta_termino')
    
    # Definimos métodos para acceder a los campos relacionados
    def prestador(self, obj):
        return obj.servicio_social.prestador.matricula # O cualquier atributo de Prestador que quieras mostrar

    def institucion(self, obj):
        return obj.servicio_social.institucion.nombre  # O cualquier atributo de Institucion que quieras mostrar

# Registramos el modelo en el admin
admin.site.register(ResumenDocumentos, ResumenDocumentosAdmin)