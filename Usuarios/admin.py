from django.contrib import admin
from .models import User, Role
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Permission


# Define la clase UserAdmin

#USERS
class UserAdmin(admin.ModelAdmin):
    list_display = ('id','username', 'first_name', 'last_name', 'email', 'address', 'image',  'role')
    filter_horizontal = ('user_permissions',)
  
    def has_add_permission(self, request):
        
        if request.user.groups.filter(name='Vendedor').exists():
            return False
        
        return True

    
    def has_change_permission(self, request, obj=None):
        
        if request.user.groups.filter(name='Vendedor').exists():
            return False
        
        return True

    
    def has_delete_permission(self, request, obj=None):
        
        if request.user.groups.filter(name='Vendedor').exists():
            return False
        
        return True

    
    def has_view_permission(self, request, obj=None):
        
        if request.user.groups.filter(name='Vendedor').exists():
            return True
       
        return super().has_view_permission(request, obj)


admin.site.register(User, UserAdmin)


class RoleAdmin(admin.ModelAdmin):
    list_display = ('id_role', 'name')


admin.site.register(Role, RoleAdmin)

