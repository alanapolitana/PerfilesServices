#!/bin/bash

# Espera hasta que la base de datos esté lista
host="$1"
shift
until nc -z -v -w30 $host 5432
do
  echo "Esperando a que la base de datos esté disponible..."
  sleep 1
done
echo "La base de datos está disponible, ejecutando migraciones..."

# Ejecuta las migraciones
python manage.py migrate
