import json
import subprocess

def cargar_seccion_ssh(ruta_archivo):
    try:
        # Leer el contenido del archivo config.json y almacenarlo en un diccionario
        with open(ruta_archivo, 'r') as archivo:
            diccionario_config = json.load(archivo)

        # Verificar si la sección 'ssh' existe en el diccionario cargado
        if "ssh" in diccionario_config:
            ssh_section = diccionario_config["ssh"]
            return ssh_section
        else:
            print("'ssh' section not found in the config file.")
            return None

    except FileNotFoundError:
        return None
    
def cargar_seccion_modbus(ruta_archivo):
    try:
        # Leer el contenido del archivo config.json y almacenarlo en un diccionario
        with open(ruta_archivo, 'r') as archivo:
            diccionario_config = json.load(archivo)

        # Verificar si la sección 'ssh' existe en el diccionario cargado
        if "modbus" in diccionario_config:
            ssh_section = diccionario_config["modbus"]
            return ssh_section
        else:
            print("'ssh' section not found in the config file.")
            return None

    except FileNotFoundError:
        return None