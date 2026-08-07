#!/usr/bin/env bash
set -o errexit

echo "==== Actualizando pip ===="
pip install --upgrade pip

echo "==== Instalando dependencias ===="
pip install -r requirements.txt

echo "==== Recolectando archivos estáticos ===="
python manage.py collectstatic --no-input

echo "==== Ejecutando migraciones ===="
python manage.py migrate --noinput

echo "==== Creando usuario administrador ===="
python manage.py crear_administrador --username admin --email admin@example.com --password Admin1234!

echo "==== Build completado exitosamente ===="