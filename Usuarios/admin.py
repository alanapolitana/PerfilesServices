from django.contrib import admin
from .models import User, Role
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Permission
#USERS
from django.contrib import admin
from .models import User  # Asegúrate de importar el modelo User
from cloudinary.forms import CloudinaryFileField
from django import forms

# Crear un formulario personalizado si es necesario
class UserAdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'

    # Puedes agregar más validaciones o personalizaciones si es necesario
class UserAdmin(admin.ModelAdmin):
    form = UserAdminForm

    list_display = ('id', 'username', 'email', 'get_image', 'is_active', 'is_staff', 'get_role')
    list_filter = ('is_active', 'is_staff', 'role')  
    search_fields = ('username', 'email')  

    fieldsets = (
        (None, {
            'fields': ('username', 'email', 'image', 'first_name', 'last_name', 'phone', 'role', 'gender')
        }),
        ('Permisos', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Fechas', {
            'fields': ('date_joined',)
        }),
    )

    def get_image(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="50" height="50"/>'
        return "Sin imagen"
    get_image.allow_tags = True
    get_image.short_description = "Imagen"

    def get_role(self, obj):
        return obj.role.name if obj.role else "Sin rol"
    get_role.short_description = "Rol"

admin.site.register(User, UserAdmin)


class RoleAdmin(admin.ModelAdmin):
    list_display = ('id_role', 'name')

admin.site.register(Role, RoleAdmin)

