""" from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Parque, Actividad, ActividadUsuario

# Configuración personalizada para el modelo Parque
class ParqueAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'ubicacion', 'descripcion', 'comentarios', 'actividades_list_display')
    search_fields = ('nombre', 'ubicacion')
    list_filter = ('ubicacion',)
    readonly_fields = ('actividades_list_display',)
    
    def actividades_list_display(self, obj):

        actividades = obj.actividades.all()
        if actividades:
            links = []
            for actividad in actividades:
                # Genera la URL para el cambio del objeto Actividad en el admin.
                url = reverse('admin:AlParque_actividad_change', args=(actividad.pk,))
                links.append(f'<a href="{url}">{actividad.nombre}</a>')
            # Marcar la cadena como segura para que se renderice el HTML
            return mark_safe(", ".join(links))
        return "No hay actividades"
    
    actividades_list_display.short_description = "Actividades"

# Configuración personalizada para el modelo Actividad
class ActividadAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'habilitado', 'administrador')
    search_fields = ('nombre', 'descripcion')
    list_filter = ('habilitado', 'administrador')

# Configuración personalizada para el modelo ActividadUsuario
class ActividadUsuarioAdmin(admin.ModelAdmin):
    list_display = ('actividad', 'user', 'integranteDesde', 'aprobado')  # Asegúrate de usar 'integranteDesde' en lugar de 'fecha_participacion'
    list_filter = ('actividad', 'user', 'aprobado')
    search_fields = ('actividad__nombre', 'user__email')

# Registrar los modelos con su configuración personalizada
admin.site.register(Parque, ParqueAdmin)
admin.site.register(Actividad, ActividadAdmin)
admin.site.register(ActividadUsuario, ActividadUsuarioAdmin)
 """
from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Parque, Actividad, ActividadUsuario
from django.utils.html import format_html

# Configuración personalizada para el modelo Parque
class ParqueAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'ubicacion', 'descripcion', 'comentarios', 'actividades_list_display')
    search_fields = ('nombre', 'ubicacion')
    list_filter = ('ubicacion',)
    readonly_fields = ('actividades_list_display',)
    
    def actividades_list_display(self, obj):
        """
        Retorna una cadena con enlaces a los usuarios aprobados de las actividades asociadas,
        separadas por comas.
        """
        actividades = obj.actividades.all()
        if actividades:
            links = []
            for actividad in actividades:
                # Genera la URL para el cambio del objeto Actividad en el admin.
                url = reverse('admin:AlParque_actividad_change', args=(actividad.pk,))
                links.append(f'<a href="{url}">{actividad.nombre}</a>')

            
            # Marcar la cadena como segura para que se renderice el HTML
            return mark_safe("<br>".join(links))
        return "No hay actividades"
    
    actividades_list_display.short_description = "Actividades"

class ActividadAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'parque', 'cantidad_usuarios_aprobados', 'correos_usuarios_aprobados_list', 'seleccionar_administrador')
    search_fields = ('nombre', 'descripcion')
    list_filter = ('parque', 'habilitado')

    def correos_usuarios_aprobados_list(self, obj):
        """
        Retorna los correos electrónicos de los usuarios aprobados en la actividad.
        """
        correos = obj.correos_usuarios_aprobados  # Obtiene la lista de correos
        if correos:
            return format_html("<br>".join(correos))  # Formatear en HTML con saltos de línea
        return "No hay usuarios aprobados"
    
    correos_usuarios_aprobados_list.short_description = "Correos Aprobados"

    def seleccionar_administrador(self, obj):
        """
        Genera un dropdown en el admin para seleccionar un administrador de la actividad.
        """
        usuarios_aprobados = obj.usuarios_aprobados
        if not usuarios_aprobados.exists():
            return "No hay usuarios aprobados"

        opciones = "".join(
            [f'<option value="{user.id}">{user.email}</option>' for user in usuarios_aprobados]
        )
        return format_html(f'<select name="admin_user">{opciones}</select>')
    
    seleccionar_administrador.short_description = "Seleccionar Administrador"
class ActividadUsuarioAdmin(admin.ModelAdmin):
    list_display = ('user', 'actividad', 'aprobado', 'administrador')
    list_filter = ('aprobado', 'actividad')
    search_fields = ('user__email', 'actividad__nombre')
    actions = ['hacer_administrador']

    def hacer_administrador(self, request, queryset):
        """
        Permite seleccionar un usuario y asignarlo como administrador de la actividad.
        """
        for obj in queryset:
            obj.administrador = True
            obj.save()
        self.message_user(request, "Administrador asignado con éxito.")

    hacer_administrador.short_description = "Hacer administrador"



# Configuración personalizada para el modelo ActividadUsuario
class ActividadUsuarioAdmin(admin.ModelAdmin):
    list_display = ('actividad', 'user', 'integranteDesde', 'aprobado')  # Asegúrate de usar 'integranteDesde' en lugar de 'fecha_participacion'
    list_filter = ('actividad', 'user', 'aprobado')
    search_fields = ('actividad__nombre', 'user__email')

# Registrar los modelos con su configuración personalizada
admin.site.register(Parque, ParqueAdmin)
admin.site.register(Actividad, ActividadAdmin)
admin.site.register(ActividadUsuario, ActividadUsuarioAdmin)
