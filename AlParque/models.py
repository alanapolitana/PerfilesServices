from django.db import models
from Usuarios.models import User
from django.core.exceptions import PermissionDenied

class Parque(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    imagenes = models.JSONField(default=list, blank=True, null=True)
    habilitado = models.BooleanField(default=False)
    ubicacion = models.CharField(max_length=255)
    comentarios = models.TextField(blank=True, null=True)
  
    def __str__(self):
        return self.nombre

class Actividad(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    imagenes = models.JSONField(default=list, blank=True)
    instagram = models.URLField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    habilitado = models.BooleanField(default=False)
    comentarios = models.TextField(blank=True, null=True)
    parque = models.ForeignKey(Parque, on_delete=models.CASCADE, related_name='actividades')

    def __str__(self):
        return self.nombre
   
    @property
    def usuarios_aprobados(self):
        """ Devuelve un queryset con los usuarios aprobados en esta actividad. """
        return User.objects.filter(actividadusuario__actividad=self, actividadusuario__aprobado=True)

    @property
    def cantidad_usuarios_aprobados(self):
        """ Devuelve el número total de usuarios aprobados en esta actividad. """
        return self.usuarios_aprobados.count()

    @property
    def correos_usuarios_aprobados(self):
        """ Devuelve una lista de los correos electrónicos de los usuarios aprobados. """
        return [user.email for user in self.usuarios_aprobados]

    def __str__(self):
        return f"{self.nombre} ({self.cantidad_usuarios_aprobados} participantes)"



class ActividadUsuario(models.Model):
    actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE, related_name='participantes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_constraint=False)
    integranteDesde = models.DateTimeField(auto_now_add=True)
    aprobado = models.BooleanField(default=False)
    administrador = models.BooleanField(default=False)

    def __str__(self):
        return f"Usuario {self.user.email} participó en {self.actividad.nombre}"

    class Meta:
        db_table = 'actividad_usuario'

    def aprobar_usuario(self, admin_user):
        """ Aprueba a un usuario para participar en la actividad. Solo un administrador puede hacerlo. """
        if not ActividadUsuario.objects.filter(actividad=self.actividad, user=admin_user, administrador=True).exists():
            raise PermissionDenied("Solo un administrador puede aprobar usuarios.")
        
        self.aprobado = True
        self.save()

    def asignar_admin(self, admin_user):
        """ Asigna permisos de administrador a otro usuario. Solo un administrador puede hacerlo. """
        if not ActividadUsuario.objects.filter(actividad=self.actividad, user=admin_user, administrador=True).exists():
            raise PermissionDenied("Solo un administrador puede asignar permisos de administrador.")

        self.administrador = True
        self.save()
