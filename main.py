import sys
import os
from SSH import function

# Obtener la ruta absoluta del archivo que llamó a main.py
ruta_llamada = os.path.abspath(os.getcwd())

# Comprobar si las peticiones vienen de SSH
if "SSH" in ruta_llamada:

    # Obtener el input del argumento de línea de comandos
    cmd_from_client = sys.argv[1]

    function.execute_cmd(cmd_from_client)

# Comprobar si las peticiones vienen de Modbus
elif "Modbus" in ruta_llamada:
    print("Protocolo Modbus")
else:
    print("No se pudo identificar el Protocolo")
