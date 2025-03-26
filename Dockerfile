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

# Instalar netcat (nc)
RUN apt-get update && apt-get install -y netcat

# Copia todos los archivos al contenedor después de instalar dependencias
COPY . .

# Crea el directorio de logs
RUN mkdir -p /Perfiles/logs

# Comando para recopilar archivos estáticos
RUN python manage.py collectstatic --noinput

# Genera las migraciones automáticamente
RUN python manage.py makemigrations

# Copia el script de espera
COPY wait-for-db.sh /usr/local/bin/wait-for-db.sh
RUN chmod +x /usr/local/bin/wait-for-db.sh

# Espera a que la base de datos esté lista y luego realiza las migraciones
RUN /usr/local/bin/wait-for-db.sh postgres_db

# Ejecuta las migraciones automáticamente
RUN python manage.py migrate

# Expone el puerto de la aplicación
EXPOSE 8000

# Comando para ejecutar la aplicación con Gunicorn y especificar el archivo de log de errores
CMD ["gunicorn", "Perfiles.wsgi:application", "--bind", "0.0.0.0:8000", "--error-logfile", "/Perfiles/logs/django_error.log"]
