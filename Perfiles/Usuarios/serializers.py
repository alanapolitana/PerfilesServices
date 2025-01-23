from rest_framework import serializers

from .models import Role, User,BMI


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer 

from decimal import Decimal
from django.utils import timezone

 

from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username', 'first_name', 'last_name', 'email', 'password', 'address', 'phone', 'image']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data.get('username', ''),      # Opcional
            first_name=validated_data.get('first_name', ''),  # Opcional
            last_name=validated_data.get('last_name', ''),    # Opcional
            email=validated_data['email'],
            address=validated_data.get('address', ''),        # Opcional
            phone=validated_data.get('phone', ''),            # Opcional
            image=validated_data.get('image')                 # Opcional
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.address = validated_data.get('address', instance.address)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.image = validated_data.get('image', instance.image)

        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)
        
        instance.save()
        return instance


class LogoutSerializer(serializers.Serializer):
    user = serializers.IntegerField()



""" class LogoutSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        # Autenticación de usuario
        user = authenticate(email=email, password=password)

        if user is None:
            raise serializers.ValidationError({"error": "No existe este usuario o las credenciales son incorrectas."})
        
        return attrs """
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        return token

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'
        
        
class BMISerializer(serializers.ModelSerializer):
    bmi = serializers.ReadOnlyField()  # Campo calculado basado en peso y altura

    class Meta:
        model = BMI
        fields = ['id_bmi', 'user', 'weight', 'height', 'date', 'bmi']
        read_only_fields = ['id_bmi', 'bmi', 'date']  # ID y fecha solo lectura

    def validate(self, data):
        # Validación para asegurar que el peso y la altura son positivos
        if data['weight'] <= 0 or data['height'] <= 0:
            raise serializers.ValidationError('El peso y la altura deben ser positivos.')
        return data