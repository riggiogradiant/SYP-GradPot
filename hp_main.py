import sys
import os
import subprocess
import concurrent.futures

from src.application.ssh import ssh_functions


# Obtener la ruta absoluta del archivo que llamó a main.py
ruta_llamada = os.path.abspath(os.getcwd())
ruta_hp_ssh = str(os.getcwd()) + "/src/application/ssh"
ruta_hp_modbus = str(os.getcwd()) + "/src/application/modbus"

#Si es la llamda de ejecución del HP
if ruta_llamada.endswith("SYP-GradPot"):

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(lambda: subprocess.run(["python3", "honeypot.py"], cwd=ruta_hp_ssh))
        executor.submit(lambda: subprocess.run(["python3", "honeypot.py"], cwd=ruta_hp_modbus))

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
    print("[Modbus] mensaje recibido del protocolo Modbus")

else: #Si no tiene ningún de esos protocolos en la petición es pq es la llamada del main que lanza el Honeypot
    print("No se pudo identificar el Protocolo")
