from rest_framework import serializers
from .models import Role, User,BMI
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer 
from decimal import Decimal
from django.utils import timezone
import cloudinary
from django.contrib.auth import authenticate
import cloudinary.uploader
import time
class UserSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)
    gender = serializers.ChoiceField(choices=User.GENDER_CHOICES, required=False)

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'phone', 'image', 'gender']
        extra_kwargs = {'password': {'write_only': True}}

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.gender = validated_data.get('gender', instance.gender)  

        # Subir la imagen solo si se proporciona una nueva
        image = validated_data.get('image', None)
        if image:
            resultado = cloudinary.uploader.upload(image, public_id=f"user_{instance.id}_{int(time.time())}", overwrite=True)
            new_image_url = resultado.get('secure_url')

            if new_image_url:
                instance.image = new_image_url

        instance.save()
        return instance



""" class UserSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'address', 'phone', 'image']

    def get_image(self, obj):
        if obj.image:
            return obj.image.url if obj.image.url.startswith('http') else f"https://res.cloudinary.com/dhufclese{obj.image.url}"
        return None """

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password', 'phone', 'image']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        image = validated_data.pop('image', None)  # Extraer imagen
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()

        if image:
            resultado = cloudinary.uploader.upload(image)
            user.image = resultado.get('secure_url')
            user.save()
        
        return user


class LogoutSerializer(serializers.Serializer):
    user = serializers.IntegerField()



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