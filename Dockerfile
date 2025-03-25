# Usa una imagen base de Python 3.12
FROM python:3.12

# Establece el directorio de trabajo en /Perfiles
WORKDIR /Perfiles

# Copia el archivo .env para las variables de entorno
COPY .env /Perfiles/.env

# Copia solo los archivos esenciales para aprovechar la caché de Docker
COPY requirements.txt /Perfiles/

# Instala las dependencias antes de copiar todo el código
RUN pip install --no-cache-dir -r requirements.txt



# Copia todos los archivos al contenedor después de instalar dependencias
COPY . .

# Crea el directorio de logs
RUN mkdir -p /Perfiles/logs

RUN python manage.py makemigrations && \
    python manage.py migrate && \
    python manage.py collectstatic --noinput


# Expone el puerto de la aplicación
EXPOSE 8000

# Comando para ejecutar la aplicación con Gunicorn y especificar el archivo de log de errores
CMD ["gunicorn", "Perfiles.wsgi:application", "--bind", "0.0.0.0:8000", "--error-logfile", "/Perfiles/logs/django_error.log"]
