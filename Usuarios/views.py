from django.http import JsonResponse
from matplotlib.lines import Line2D
import pandas as pd
from rest_framework import status, permissions,generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from django.contrib.auth import authenticate

from Usuarios.bmi_chart import generate_bmi_dataframe
from .serializers import RoleSerializer, UserSerializer, CustomTokenObtainPairSerializer, LogoutSerializer,BMISerializer
from .models import Role, User,BMI
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet
from django.http import HttpResponse
import io
import matplotlib
matplotlib.use('Agg')  # Usa el backend sin GUI
import matplotlib.pyplot as plt
from Usuarios import serializers
import pandas as pd
import matplotlib.pyplot as plt
import io
from django.http import HttpResponse
from rest_framework.views import APIView
from .bmi_chart import generate_bmi_dataframe
from decimal import Decimal
import mplcursors  # Importar la librería para el hover
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from io import BytesIO
import cloudinary
class RegisterView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Login(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get('email', '')
        password = request.data.get('password', '')
        user = authenticate(email=email, password=password)

        if user:
            login_serializer = self.serializer_class(data=request.data)
            if login_serializer.is_valid():
                user_serializer = UserSerializer(user)
                return Response({
                    'token': login_serializer.validated_data['access'],
                    'refresh-token': login_serializer.validated_data['refresh'],
                    'user': user_serializer.data,
                    'message': 'Inicio de Sesión Exitoso'
                }, status=status.HTTP_200_OK)
            return Response({'error': 'Contraseña o nombre de usuario incorrectos'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Contraseña o nombre de usuario incorrectos'}, status=status.HTTP_400_BAD_REQUEST)

""" class Login(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response({"error": "Correo o contraseña incorrectos"}, status=status.HTTP_400_BAD_REQUEST)
 """
class Logout(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LogoutSerializer

    def post(self, request, *args, **kwargs):
        user = User.objects.filter(id=request.data.get('user', 0))
        if user.exists():
            RefreshToken.for_user(user.first())
            return Response({'message': 'Sesión cerrada correctamente.'}, status=status.HTTP_200_OK)
        return Response({'error': 'No existe este usuario.'}, status=status.HTTP_400_BAD_REQUEST)

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import User
from .serializers import UserSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

class UserUpdateView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def patch(self, request):
        user = request.user
        image = request.data.get('image')

        if image:
            user.image = image
            user.save()
            return Response({"image": user.image.url}, status=status.HTTP_200_OK)

        return Response({"image": ["Este campo es requerido."]}, status=status.HTTP_400_BAD_REQUEST)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    parser_classes = [MultiPartParser, FormParser]

    def create(self, request, *args, **kwargs):
        imagenes_urls = []

        if request.FILES.getlist('image'):
            for imagen in request.FILES.getlist('image'):
                resultado = cloudinary.uploader.upload(imagen)
                imagenes_urls.append(resultado['secure_url'])

        # Combinar imágenes en la data original
        data = request.data.dict()
        data['image'] = imagenes_urls

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data.copy()

        image_urls = instance.image or []
        if 'image' in request.FILES:
            for imagen in request.FILES.getlist('image'):
                resultado = cloudinary.uploader.upload(imagen)
                imagenes_urls.append(resultado['secure_url'])

        data['image'] = image_urls

        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

 
""" from .serializers import LogoutSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from django.contrib.auth import logout
class Logout(APIView):
    def post(self, request):
        # Serializamos los datos del request
        serializer = LogoutSerializer(data=request.data)

        if serializer.is_valid():
            # Realizamos el logout del usuario
            logout(request)
            return Response({"message": "Cierre de sesión exitoso."}, status=HTTP_200_OK)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
         """
class UserView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class UpdateUserView(APIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
    
    def patch(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.serializer_class(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RoleViewSet(ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAdminUser]

""" class BMICreateAPIView(generics.CreateAPIView):

    serializer_class = BMISerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user) """

class BMICreateAPIView(generics.CreateAPIView):
    """
    Endpoint para que el usuario registre su IMC.
    """
    serializer_class = BMISerializer
    permission_classes = [permissions.IsAuthenticated]  # Requiere autenticación

    def perform_create(self, serializer):
        # Asegúrate de que el usuario esté autenticado antes de guardar
        if not self.request.user.is_authenticated:
            raise serializers.ValidationError("Usuario no autenticado.")
        
        serializer.save(user=self.request.user)  # Asocia al usuario logueado
class BMIListAPIView(generics.ListAPIView):
    """
    Endpoint para listar los registros de IMC del usuario actual.
    """
    serializer_class = BMISerializer
    permission_classes = [permissions.IsAuthenticated]  # Solo accesible para usuarios autenticados

    def get_queryset(self):
        # Asegúrate de que el usuario esté autenticado antes de realizar la consulta
        if not self.request.user.is_authenticated:
            raise serializers.ValidationError("Usuario no autenticado.")
        
        return BMI.objects.filter(user=self.request.user)  # Filtrar por usuario logueado

   
def view_imc(request, user_id):
    # Verifica que el usuario esté autenticado antes de acceder a los datos
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Usuario no autenticado'}, status=401)

    # Verifica si el usuario está intentando acceder a su propio IMC
    if request.user.id != user_id:
        return JsonResponse({'error': 'No tienes permiso para acceder a este IMC'}, status=403)

    try:
        bmi = BMI.objects.get(user_id=user_id)
        return JsonResponse({'user_id': user_id, 'imc': bmi.imc})
    except BMI.DoesNotExist:
        return JsonResponse({'error': 'IMC no encontrado para este usuario'}, status=404)

class BMIChartView(APIView):
    """
    Endpoint para generar un gráfico de IMC por usuario en el tiempo.
    """
    def get(self, request):
        # Generar el DataFrame (puedes definir la función generate_bmi_dataframe() según tu lógica)
        df = generate_bmi_dataframe()

        # Verificar las columnas del DataFrame para asegurarnos de que 'User' existe
        print(df.columns)  # Esto mostrará todas las columnas del DataFrame

        # Filtrar registros del usuario logueado
        if 'User' not in df.columns:
            return HttpResponse("La columna 'User' no se encuentra en los datos.", status=400)

        user_data = df[df['User'] == request.user.email]

        if user_data.empty:
            return HttpResponse("No hay datos de IMC para el usuario logueado.", status=404)

        # Asegúrate de que la columna 'Date' sea de tipo datetime
        user_data['Date'] = pd.to_datetime(user_data['Date'], errors='coerce')
        user_data = user_data.dropna(subset=['Date']).sort_values(by='Date')

        # Definir los colores según el IMC con subcategorías
        def get_bmi_color(bmi):
            if bmi < 18.5:
                return 'red'  # Bajo peso
            elif 18.5 <= bmi < 24.9:
                return 'green'  # Saludable
            elif 25 <= bmi < 27:
                return 'yellow'  # Sobrepeso grado I
            elif 27 <= bmi < 30:
                return 'orange'  # Sobrepeso grado II
            elif 30 <= bmi < 35:
                return 'purple'  # Obesidad grado I
            elif 35 <= bmi < 40:
                return 'darkviolet'  # Obesidad grado II
            else:
                return 'brown'  # Obesidad grado III (Mórbida)

        user_data['Color'] = user_data['BMI'].apply(get_bmi_color)

        # Calcular el peso ideal (IMC = 21.7)
        def calculate_ideal_weight(height):
            # Convertir la altura a float si es un decimal
            height = float(height) if isinstance(height, Decimal) else height
            return 21.7 * (height ** 2)

        # Calcular el peso ideal para cada registro
        user_data['IdealWeight'] = user_data['Height'].apply(calculate_ideal_weight)

        # Crear el gráfico
        plt.figure(figsize=(10, 6))

        # Graficar la línea continua que conecta los puntos
        plt.plot(user_data['Date'], user_data['BMI'], color='gray', linestyle='-', linewidth=1, alpha=0.7)

        # Graficar los puntos de IMC con colores definidos
        scatter = plt.scatter(user_data['Date'], user_data['BMI'], c=user_data['Color'], s=100, edgecolors='k', alpha=0.7)

        # Modificado: Añadir etiquetas de IMC y peso en cada punto
        for i, row in user_data.iterrows():
            plt.text(row['Date'], row['BMI'], f'IMC: {row["BMI"]:.1f}\n {row["Weight"]} kg', 
                     fontsize=9, ha='center', va='bottom')

        # Graficar la línea del peso ideal (IMC de 21.7)
        plt.axhline(y=21.7, color='blue', linestyle='--', label='Peso Ideal (IMC = 21.7)')

        # Añadir líneas para las categorías de IMC
        plt.axhline(y=18.5, color='lightgray', linestyle='--', label='Bajo peso (IMC < 18.5)')
        plt.axhline(y=24.9, color='lightgreen', linestyle='--', label='Peso saludable (18.5 ≤ IMC < 24.9)')
        plt.axhline(y=25, color='yellow', linestyle='--', label='Sobrepeso grado I (25 ≤ IMC < 27)')
        plt.axhline(y=27, color='orange', linestyle='--', label='Sobrepeso grado II (27 ≤ IMC < 30)')
        plt.axhline(y=30, color='purple', linestyle='--', label='Obesidad grado I (30 ≤ IMC < 35)')
        plt.axhline(y=35, color='darkviolet', linestyle='--', label='Obesidad grado II (35 ≤ IMC < 40)')
        plt.axhline(y=40, color='brown', linestyle='--', label='Obesidad grado III (IMC ≥ 40)')

        # Etiquetas y configuración
        plt.xlabel('Fecha')
        plt.ylabel('IMC')
        plt.title('Evolución del IMC')

        # Añadir leyenda explicativa de colores, fuera del gráfico
        legend_elements = [
            Line2D([0], [0], marker='o', color='w', label='Bajo peso (IMC < 18.5)', markerfacecolor='red', markersize=10, alpha=0.7),
            Line2D([0], [0], marker='o', color='w', label='Saludable (18.5 ≤ IMC < 24.9)', markerfacecolor='green', markersize=10, alpha=0.7),
            Line2D([0], [0], marker='o', color='w', label='Sobrepeso grado I (25 ≤ IMC < 27)', markerfacecolor='yellow', markersize=10, alpha=0.7),
            Line2D([0], [0], marker='o', color='w', label='Sobrepeso grado II (27 ≤ IMC < 30)', markerfacecolor='orange', markersize=10, alpha=0.7),
            Line2D([0], [0], marker='o', color='w', label='Obesidad grado I (30 ≤ IMC < 35)', markerfacecolor='purple', markersize=10, alpha=0.7),
            Line2D([0], [0], marker='o', color='w', label='Obesidad grado II (35 ≤ IMC < 40)', markerfacecolor='darkviolet', markersize=10, alpha=0.7),
            Line2D([0], [0], marker='o', color='w', label='Obesidad grado III (IMC ≥ 40)', markerfacecolor='brown', markersize=10, alpha=0.7),
            Line2D([0], [0], color='blue', linestyle='--', label='Peso Ideal (IMC = 21.7)', markersize=10, alpha=0.7)
        ]

        # Ajustar la leyenda fuera del gráfico
        plt.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(1, 1), borderaxespad=1)

        # Activar el cursor interactivo para mostrar el valor del IMC
        cursor = mplcursors.cursor(scatter, hover=True)
        cursor.connect("add", lambda sel: sel.annotation.set_text(f'IMC: {user_data.iloc[sel.target.index]["BMI"]:.1f}\nPeso: {user_data.iloc[sel.target.index]["Weight"]} kg'))

        plt.grid(True)
        plt.tight_layout()

        # Guardar el gráfico en un buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close()

        # Devolver el gráfico como respuesta HTTP
        return HttpResponse(buf, content_type='image/png')


class ExportBMICSVView(APIView):
    """
    Endpoint para exportar datos de IMC en formato PDF.
    """
    def get(self, request):
        df = generate_bmi_dataframe()

        # Crear un buffer para generar el PDF
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=letter)

        # Configurar el título del documento
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(50, 750, "Datos de IMC")

        # Configurar el encabezado de la tabla
        pdf.setFont("Helvetica-Bold", 12)
        x_offset = 50
        y_offset = 700
        line_height = 20

        for idx, column in enumerate(df.columns):
            pdf.drawString(x_offset + idx * 100, y_offset, column)

        # Agregar los datos al PDF
        pdf.setFont("Helvetica", 10)
        y_offset -= line_height
        for _, row in df.iterrows():
            for idx, value in enumerate(row):
                pdf.drawString(x_offset + idx * 100, y_offset, str(value))
            y_offset -= line_height
            if y_offset < 50:  # Añadir una nueva página si se acaba el espacio
                pdf.showPage()
                y_offset = 750

        # Finalizar el PDF
        pdf.save()

        # Configurar la respuesta HTTP para enviar el PDF
        buffer.seek(0)
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="bmi_data.pdf"'
        return response
