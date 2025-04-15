from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Parque, Actividad, ActividadUsuario

### --- PARQUE ADMIN --- ###
@admin.register(Parque)
class ParqueAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'ubicacion', 'descripcion', 'comentarios', 'actividades_list_display')
    search_fields = ('nombre', 'ubicacion')
    list_filter = ('ubicacion',)
    readonly_fields = ('actividades_list_display',)

    def actividades_list_display(self, obj):
        actividades = obj.actividades.all()
        if not actividades:
            return "No hay actividades"
        
        links = [
            format_html('<a href="{}">{}</a>', 
                        reverse('admin:AlParque_actividad_change', args=[actividad.pk]), 
                        actividad.nombre)
            for actividad in actividades
        ]
        return format_html("<br>".join(links))

    actividades_list_display.short_description = "Actividades"

### --- ACTIVIDAD ADMIN --- ###
@admin.register(Actividad)
class ActividadAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion', 'parque', 'cantidad_usuarios_aprobados', 'correos_aprobados', 'admins_aprobados']

    def cantidad_usuarios_aprobados(self, obj):
        return obj.participantes.filter(aprobado=True).count()
    cantidad_usuarios_aprobados.short_description = 'Usuarios aprobados'

    def correos_aprobados(self, obj):
        usuarios = obj.participantes.filter(aprobado=True).select_related('user')
        return ', '.join([u.user.email for u in usuarios]) if usuarios else 'Ninguno'
    correos_aprobados.short_description = 'Correos aprobados'

    def admins_aprobados(self, obj):
        admins = obj.participantes.filter(aprobado=True, administrador=True).select_related('user')
        nombres = []
        for a in admins:
            user = a.user
            full_name = f"{getattr(user, 'first_name', '')} {getattr(user, 'last_name', '')}".strip()
            nombres.append(full_name if full_name else user.username or user.email)
        return ', '.join(nombres) if nombres else 'Ninguno'
    admins_aprobados.short_description = 'Admins aprobados'

### --- ACTIVIDAD USUARIO ADMIN --- ###
@admin.register(ActividadUsuario)
class ActividadUsuarioAdmin(admin.ModelAdmin):
    list_display = ['actividad', 'user_display', 'integranteDesde', 'aprobado_icon', 'administrador_icon']
    search_fields = ['actividad__nombre', 'user__username', 'user__email']
    list_filter = ['aprobado', 'administrador']

    def user_display(self, obj):
        user = obj.user
        full_name = f"{getattr(user, 'first_name', '')} {getattr(user, 'last_name', '')}".strip()
        return full_name if full_name else user.username or user.email
    user_display.short_description = "Usuario"

    def aprobado_icon(self, obj):
        icon = "✅" if obj.aprobado else "❌"
        return format_html(f"<span>{icon}</span>")
    aprobado_icon.short_description = "Aprobado"

    def administrador_icon(self, obj):
        icon = "👑" if obj.administrador else "—"
        return format_html(f"<span>{icon}</span>")
    administrador_icon.short_description = "Administrador"

