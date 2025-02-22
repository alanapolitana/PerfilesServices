# urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import  ParqueViewSet, ActividadViewSet, RegistrarUsuarioActividad

router = DefaultRouter()
router.register(r'parques', ParqueViewSet)
router.register(r'actividades', ActividadViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('actividades/registrar/<int:actividad_id>/', RegistrarUsuarioActividad.as_view(), name='registrar_usuario_actividad'),  # Ruta para registrar usuario

]
