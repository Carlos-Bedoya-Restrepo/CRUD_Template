# CRUD_Template
This is a fairly complete template that allows me to generate communication with frontend, backend and database

# Uso de la aplicacion
git clone <directory>
## Create virtual machine
-->windows: python -m venv env_name
-->Ubuntu: python3 -m venv env_name
## Activar/desactivar virtual machine
-->windows: env_name/Scipts/activate
            deactivate
-->Ubuntu: source env_name/bin/activate
            deactivate
## Instalacion de recursos
pip3 install -r requirements.txt
## Correr aplicacion
uvicorn app.main:app -reload

