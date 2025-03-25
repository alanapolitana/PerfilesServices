import cloudinary.uploader
from rest_framework import serializers, viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Parque, Actividad, ActividadUsuario
from .serializers import ParqueSerializer, ActividadSerializer, ActividadUsuarioSerializer
from rest_framework import status, generics
from django_filters.rest_framework import DjangoFilterBackend
from django.core.exceptions import PermissionDenied

class ParqueViewSet(viewsets.ModelViewSet):
    queryset = Parque.objects.all()
    serializer_class = ParqueSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def create(self, request, *args, **kwargs):
        imagenes_urls = []

        if request.FILES.getlist('imagenes'):
            for imagen in request.FILES.getlist('imagenes'):
                resultado = cloudinary.uploader.upload(imagen)
                imagenes_urls.append(resultado['secure_url'])

        data = request.data.dict()
        data['imagenes'] = imagenes_urls

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        imagenes_urls = instance.imagenes if instance.imagenes else []

        if request.FILES.getlist('imagenes'):
            for imagen in request.FILES.getlist('imagenes'):
                resultado = cloudinary.uploader.upload(imagen)
                imagenes_urls.append(resultado['secure_url'])

        data = request.data.dict()
        data['imagenes'] = imagenes_urls

        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
class ActividadViewSet(viewsets.ModelViewSet):
    queryset = Actividad.objects.all()
    serializer_class = ActividadSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields  = ['parque']
    
    def create(self, request, *args, **kwargs):
        imagenes_urls = []

        if request.FILES.getlist('imagenes'):
            for imagen in request.FILES.getlist('imagenes'):
                resultado = cloudinary.uploader.upload(imagen)
                imagenes_urls.append(resultado['secure_url'])

        data = request.data.dict()
        data['imagenes'] = imagenes_urls

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        imagenes_urls = instance.imagenes if instance.imagenes else []

        if request.FILES.getlist('imagenes'):
            for imagen in request.FILES.getlist('imagenes'):
                resultado = cloudinary.uploader.upload(imagen)
                imagenes_urls.append(resultado['secure_url'])

        data = request.data.dict()
        data['imagenes'] = imagenes_urls

        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)





class ActividadUsuarioViewSet(viewsets.ModelViewSet):
    queryset = ActividadUsuario.objects.all()
    serializer_class = ActividadUsuarioSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """ 
        Al crear una relación usuario-actividad, la aprobación es manual.
        """
        serializer.save(aprobado=False, administrador=False)

    @action(detail=True, methods=['patch'], url_path='aprobar')
    def aprobar_usuario(self, request, pk=None):
        """
        Permite a un administrador aprobar a un usuario en la actividad.
        """
        actividad_usuario = self.get_object()

        # Verificar si el usuario actual es admin de la actividad
        if not ActividadUsuario.objects.filter(
            actividad=actividad_usuario.actividad, user=request.user, administrador=True
        ).exists():
            raise PermissionDenied("Solo un administrador puede aprobar usuarios.")

        actividad_usuario.aprobado = True
        actividad_usuario.save()
        return Response({"message": "Usuario aprobado exitosamente."})

    @action(detail=True, methods=['patch'], url_path='hacer-admin')
    def hacer_admin(self, request, pk=None):
        """
        Permite a un administrador asignar a otro usuario como administrador.
        """
        actividad_usuario = self.get_object()

        # Verificar si el usuario actual es admin de la actividad
        if not ActividadUsuario.objects.filter(
            actividad=actividad_usuario.actividad, user=request.user, administrador=True
        ).exists():
            raise PermissionDenied("Solo un administrador puede asignar administradores.")

        actividad_usuario.administrador = True
        actividad_usuario.save()
        return Response({"message": "Usuario ahora es administrador."})
