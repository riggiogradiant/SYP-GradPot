import sys
import os
from src.application.ssh import ssh_functions


# Obtener la ruta absoluta del archivo que llamó a main.py
ruta_llamada = os.path.abspath(os.getcwd())


# Comprobar si las peticiones vienen de SSH
if "ssh" in ruta_llamada:
    # Obtener el input del argumento de línea de comandos
    command = sys.argv[1]
    client_ip = sys.argv[2]
    username = sys.argv[3]
    ssh_functions.handle_cmd(command, client_ip, username)
# Comprobar si las peticiones vienen de Modbus
elif "modbus" in ruta_llamada:
    
    print("Protocolo Modbus")
else:
    print("No se pudo identificar el Protocolo")