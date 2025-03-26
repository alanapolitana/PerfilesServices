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


# Instala el cliente de PostgreSQL
RUN apt-get update && apt-get install -y postgresql-client
# Copia todos los archivos al contenedor después de instalar dependencias
COPY . .

# Crea el directorio de logs
RUN mkdir -p /Perfiles/logs

#Copia los archivos SQL necesarios para inicializar las bases de datos
COPY Usuarios/initial_data.sql /Perfiles/Usuarios/initial_data.sql
COPY AlParque/initial_data.sql /Perfiles/AlParque/initial_data.sql

# Comando para recopilar archivos estáticos
RUN python manage.py collectstatic --noinput

# Genera las migraciones automáticamente
RUN python manage.py makemigrations

# Ejecuta las migraciones automáticamente
RUN python manage.py migrate

# Ejecuta los scripts SQL para inicializar las bases de datos usando la URL de la base de datos
# Usamos la variable DATABASE_URL para conectarnos
RUN psql $DATABASE_URL -f /Perfiles/Usuarios/initial_data.sql
RUN psql $DATABASE_URL -f /Perfiles/AlParque/initial_data.sql

# Expone el puerto de la aplicación
EXPOSE 8000

# Comando para ejecutar la aplicación con Gunicorn y especificar el archivo de log de errores
CMD ["gunicorn", "Perfiles.wsgi:application", "--bind", "0.0.0.0:8000", "--error-logfile", "/Perfiles/logs/django_error.log"]
