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

class RegistrarUsuarioActividad(generics.CreateAPIView):
    serializer_class = ActividadUsuarioSerializer
    permission_classes = [IsAuthenticated]  # Solo usuarios autenticados pueden registrarse

    def post(self, request, actividad_id, *args, **kwargs):
        # Verificar si la actividad existe
        try:
            actividad = Actividad.objects.get(id=actividad_id)
        except Actividad.DoesNotExist:
            return Response({"detail": "La actividad no existe."}, status=status.HTTP_404_NOT_FOUND)

        # Verificar si el usuario ya está registrado
        if ActividadUsuario.objects.filter(actividad=actividad, user=request.user).exists():
            return Response({"detail": "Ya estás registrado en esta actividad."}, status=status.HTTP_400_BAD_REQUEST)

        # Crear la instancia de ActividadUsuario con la participación pendiente (aprobado=False)
        actividad_usuario = ActividadUsuario.objects.create(
            actividad=actividad,
            user=request.user,
            aprobado=False  # El administrador debe aprobarlo más tarde
        )

        return Response(ActividadUsuarioSerializer(actividad_usuario).data, status=status.HTTP_201_CREATED)