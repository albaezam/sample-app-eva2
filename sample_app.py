#!/bin/bash
export PATH=$PATH:/usr/bin:/usr/local/bin

echo "Iniciando despliegue de la aplicación de muestra"
pwd
ls -la

echo "Validando versión de Python"
/usr/bin/python3 --version

echo "Instalando Flask si es necesario"
/usr/bin/pip3 install flask --quiet || true

echo "Deteniendo ejecución previa de la aplicación"
pkill -f sample_app.py || true
sleep 2

echo "Iniciando aplicación Flask en segundo plano"
nohup /usr/bin/python3 sample_app.py > sample_app.log 2>&1 &
APP_PID=$!
disown $APP_PID

sleep 8

echo "Mostrando log de la aplicación"
cat sample_app.log

echo "Validando aplicación en puerto 9999"
curl -I http://localhost:9999

echo "Despliegue completado exitosamente"
exit 0
