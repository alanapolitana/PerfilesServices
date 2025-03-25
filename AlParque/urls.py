# urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import  ParqueViewSet, ActividadViewSet, ActividadUsuarioViewSet

router = DefaultRouter()
router.register(r'parques', ParqueViewSet)
router.register(r'actividades', ActividadViewSet)
router.register(r'actividad-usuarios', ActividadUsuarioViewSet)

urlpatterns = [
    path('', include(router.urls)),

]
