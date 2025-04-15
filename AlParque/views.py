from urllib import request
import cloudinary.uploader
from rest_framework import serializers, viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.core.exceptions import PermissionDenied

from .models import Parque, Actividad, ActividadUsuario
from .serializers import ParqueSerializer, ActividadSerializer, ActividadUsuarioSerializer
from Usuarios.models import User


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
    filterset_fields = ['parque']

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


class ActividadUsuarioViewSet(viewsets.ModelViewSet):
    queryset = ActividadUsuario.objects.all()
    serializer_class = ActividadUsuarioSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        actividad = serializer.validated_data['actividad']

        # Verifica si el usuario ya está inscrito en la actividad
        if ActividadUsuario.objects.filter(user=user, actividad=actividad).exists():
            raise serializers.ValidationError("Ya te has inscrito en esta actividad.")

        serializer.save(user=user, aprobado=False, administrador=False)

    @action(detail=True, methods=['patch'], url_path='aprobar')
    def aprobar_usuario(self, request, pk=None):
        actividad_usuario = self.get_object()

        if not ActividadUsuario.objects.filter(
            actividad=actividad_usuario.actividad, user=request.user, administrador=True
        ).exists():
            raise PermissionDenied("Solo un administrador puede aprobar usuarios.")

        actividad_usuario.aprobado = True
        actividad_usuario.save()
        return Response({"message": "Usuario aprobado exitosamente."})

    @action(detail=True, methods=['patch'], url_path='rechazar')
    def rechazar_usuario(self, request, pk=None):
        actividad_usuario = self.get_object()

        if not ActividadUsuario.objects.filter(
            actividad=actividad_usuario.actividad, user=request.user, administrador=True
        ).exists():
            raise PermissionDenied("Solo un administrador puede rechazar usuarios.")

        actividad_usuario.delete()
        return Response({"message": "Usuario rechazado correctamente."})

    @action(detail=False, methods=['get'], url_path='pendientes')
    def solicitudes_pendientes(self, request):
        actividad_id = request.query_params.get('actividad_id')
        if not actividad_id:
            return Response({"error": "Debes indicar una actividad"}, status=400)

        if not ActividadUsuario.objects.filter(
            actividad_id=actividad_id, user=request.user, administrador=True
        ).exists():
            raise PermissionDenied("Solo un administrador puede ver solicitudes pendientes.")

        pendientes = ActividadUsuario.objects.filter(actividad_id=actividad_id, aprobado=False)
        serializer = self.get_serializer(pendientes, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['patch'], url_path='hacer-admin')
    def hacer_admin(self, request, pk=None):
        actividad_usuario = self.get_object()

        if not ActividadUsuario.objects.filter(
            actividad=actividad_usuario.actividad, user=request.user, administrador=True
        ).exists():
            raise PermissionDenied("Solo un administrador puede asignar administradores.")

        actividad_usuario.administrador = True
        actividad_usuario.save()
        return Response({"message": "Usuario ahora es administrador."})
