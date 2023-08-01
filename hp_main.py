import sys
import os
import subprocess
sys.path.append("/home/criggio/OWN_HONEYPOT/src/application/configuration")
from src.application.ssh import ssh_functions


# Obtener la ruta absoluta del archivo que llamó a main.py
ruta_llamada = os.path.abspath(os.getcwd())
ruta_hp = os.getcwd() + "/src/application/ssh"
# print(ruta_llamada)

#Si es la llamda de ejecución del HP
if ruta_llamada.endswith("OWN_HONEYPOT"):
    os.chdir(ruta_hp)
    subprocess.run(["python3", "honeypot.py"])
# Comprobar si las peticiones vienen de SSH
elif "ssh" in ruta_llamada:
    # Obtener el input del argumento de línea de comandos
    command = sys.argv[1]
    client_ip = sys.argv[2]
    username = sys.argv[3]
    os.chdir(ruta_llamada)
    ssh_functions.handle_cmd(command, client_ip, username)
# Comprobar si las peticiones vienen de Modbus
elif "modbus" in ruta_llamada:
    
    print("Protocolo Modbus")
else: #Si no tiene ningún de esos protocolos en la petición es pq es la llamada del main que lanza el Honeypot
    print("No se pudo identificar el Protocolo")
