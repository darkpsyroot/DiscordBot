#!/bin/bash
#./crear_activar_venv.sh

# Crear entorno virtual llamado 'venv'
python3 -m venv venv

# Activar el entorno virtual
source venv/bin/activate

# Mostrar mensaje de confirmación
echo "Entorno virtual 'venv' activado."
