from rest_framework import serializers
from .models import Parque, Actividad, ActividadUsuario
from rest_framework import serializers
from .models import Parque

from Usuarios.serializers import UserSerializer



class ParqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parque
        fields = ['id','nombre', 'descripcion', 'ubicacion', 'imagenes', 'comentarios']

    # Si las imágenes son archivos, manejarlas con ImageField
    imagenes = serializers.ListField(child=serializers.CharField())

class ActividadSerializer(serializers.ModelSerializer):
    parque = serializers.PrimaryKeyRelatedField(queryset=Parque.objects.all())

    class Meta:
        model = Actividad
        fields = '__all__'

    def create(self, validated_data):
        parque_id = validated_data.pop('parque').id
        actividad = Actividad.objects.create(**validated_data, parque_id=parque_id)
        return actividad

    def update(self, instance, validated_data):
        parque = validated_data.pop('parque', None)
        if parque:
            instance.parque_id = parque.id
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return 
    
from rest_framework import serializers
from .models import ActividadUsuario, Actividad, User

class ActividadUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActividadUsuario
        fields = ['actividad', 'user', 'integranteDesde', 'aprobado']

    def create(self, validated_data):
        # Aquí puedes agregar lógica adicional si es necesario.
        return ActividadUsuario.objects.create(**validated_data)