from rest_framework import serializers
from .models import Parque, Actividad, ActividadUsuario
from Usuarios.models import User

class ParqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parque
        fields = ['id', 'nombre', 'descripcion', 'ubicacion', 'imagenes', 'comentarios', 'habilitado']

    # Si las imágenes son archivos, manejarlas con ImageField o String si son URLs
    imagenes = serializers.ListField(child=serializers.CharField())


class ActividadSerializer(serializers.ModelSerializer):
    parque = serializers.PrimaryKeyRelatedField(queryset=Parque.objects.all())

    class Meta:
        model = Actividad
        fields = '__all__'

    def create(self, validated_data):
        parque = validated_data.pop('parque')
        user = self.context['request'].user

        actividad = Actividad.objects.create(**validated_data, parque=parque)

        # Creamos la relación solo si no existe
        actividad_usuario, created = ActividadUsuario.objects.get_or_create(
            actividad=actividad,
            user=user,
            defaults={
                'administrador': True,
                'aprobado': False  # Podés poner True si querés que se autoapruebe
            }
        )

        # Si ya existía pero no era admin, lo marcamos como admin (opcional)
        if not created and not actividad_usuario.administrador:
            actividad_usuario.administrador = True
            actividad_usuario.save()

        return actividad

    def update(self, instance, validated_data):
        parque = validated_data.pop('parque', None)
        if parque:
            instance.parque = parque
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class ActividadUsuarioSerializer(serializers.ModelSerializer):
    actividad_id = serializers.PrimaryKeyRelatedField(
        queryset=Actividad.objects.all(),
        source='actividad',
        write_only=True
    )
    actividad = serializers.StringRelatedField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = ActividadUsuario
        fields = [
            'id', 'actividad_id', 'actividad', 'user',
            'aprobado', 'administrador', 'integranteDesde'
        ]
        read_only_fields = ['aprobado', 'administrador', 'integranteDesde']
