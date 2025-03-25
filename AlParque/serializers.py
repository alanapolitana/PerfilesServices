from rest_framework import serializers
from .models import Parque, Actividad, ActividadUsuario

class ParqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parque
        fields = ['id','nombre', 'descripcion', 'ubicacion', 'imagenes', 'comentarios','habilitado']

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
    

""" 
class ActividadUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActividadUsuario
        fields = ['id', 'actividad', 'user', 'integranteDesde', 'aprobado', 'administrador']
 """
class ActividadUsuarioSerializer(serializers.ModelSerializer):
    actividad = ActividadSerializer(read_only=True)  # Usar el serializer de actividad

    class Meta:
        model = ActividadUsuario
        fields = '__all__'
