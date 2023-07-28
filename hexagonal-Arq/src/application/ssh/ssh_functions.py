import logging
import os
import subprocess
import textwrap
import sys

ACTUAL_PATH = os.getcwd()
CONFIG_FILE = os.path.join(ACTUAL_PATH, '../../../', 'config.json')
CONFIG_FILE = os.path.normpath(CONFIG_FILE)


# Codigo necesario para importar funcion del load_config
DIR_SSH= os.path.join(ACTUAL_PATH, "..", "ssh")
DIR_SSH = os.path.normpath(DIR_SSH)
DIR_APP = os.path.join(DIR_SSH, "..")
DIR_APP = os.path.normpath(DIR_APP)
sys.path.append(DIR_APP)
from configuration.load_config import cargar_seccion_ssh

ssh_dict = cargar_seccion_ssh(CONFIG_FILE)

def handle_cmd(cmd, ip, username):

    HP_WORKING_DIR = obtener_working_dir()

    response = ""
    if cmd.startswith("ls"):
        ejecutar_comando_en_directorio(cmd, HP_WORKING_DIR)
        printear_respuesta_archivo(cmd)
    elif cmd == "pwd":
        
        xtra = pwd_get_dir()
        response = "/root" + xtra
        if response.endswith(".") or response.endswith("/"):
            response = response[:-1]

    elif cmd.startswith("cd"):
        cd_dealer(cmd)
    
    elif cmd == "whoami":
        response = username
    
    else:
        #Lo que se va a ejecutar si es otro comando
        ejecutar_comando_en_directorio(cmd, HP_WORKING_DIR)
        printear_respuesta_archivo(cmd)
        

    if response != '':
        logging.info('Response from honeypot ({}): {}'.format(ip, response))
        response = response + "\r\n"
        print(response)


# Función para ejecutar un comando en un directoio concreto 
def ejecutar_comando_en_directorio(comando, directorio):

    ssh_functions_out_dir = os.path.normpath(ACTUAL_PATH +"/" + ssh_dict['ssh_functions_out']) 
   

    try:
    
        # Utilizamos el método `run` de subprocess para ejecutar el comando en el directorio indicado
        resultado = subprocess.run(comando, shell=True, cwd=directorio, stdout=subprocess.PIPE, text=True)

        # Capturamos el código de retorno del comando
        codigo_retorno = resultado.returncode

        if codigo_retorno == 0:
            # El comando se ejecutó correctamente, escribir la salida en el archivo
            with open(ssh_functions_out_dir, "w") as archivo_salida:
                archivo_salida.write(resultado.stdout)
        else:
            # Hubo un error al ejecutar el comando
            return f"Error al ejecutar el comando. Código de retorno: {codigo_retorno}\n{resultado.stderr}"

    except Exception as e:
        return f"Error: {e}"

# Función para pillar la info del output
def printear_respuesta_archivo(cmd):
    respuesta = []
    
    ssh_functions_out_dir = os.path.normpath(ACTUAL_PATH +"/" + ssh_dict['ssh_functions_out']) 
    

    try:
        with open(ssh_functions_out_dir, "r") as archivo_salida:
            for linea in archivo_salida:
                # Procesar cada línea para eliminar los espacios en blanco al principio
                linea_procesada = linea.strip()
                respuesta.append(linea_procesada)

    except Exception as e:
        logging.error("Error al leer el archivo '{}': {}".format(ssh_functions_out_dir, e))
        print("Error al leer la salida del comando.")

    # Limpiar el contenido del archivo
    try:
        with open(ssh_functions_out_dir, "w") as archivo_salida:
            archivo_salida.write('')
    except Exception as e:
        logging.error("Error al limpiar el archivo '{}': {}".format(ssh_functions_out_dir, e))

    # Imprimir la respuesta en una sola línea separada por espacios
    if cmd == "ps":
        # Combinar todas las líneas en una sola cadena separada por saltos de línea ("\n")
        respuesta = "\n".join(respuesta)
        # Reemplazar las comas (",") por saltos de línea ("\n")
        respuesta = respuesta.replace(",", "\r\n")
        respuesta = textwrap.dedent(respuesta)
        print(respuesta)
    else:
        print("   ".join(respuesta))

# Función para lidiar con los cambios de directorio
def cd_dealer(cmd):
    directorio = cmd.split("cd ")[1].strip()
    
    log_dir = ssh_dict['log_dir']

    try:
    # Leer la primera línea del archivo y asignarla a una variable
        with open(log_dir, "r") as file:
            primera_linea = file.readline().strip()

        primera_linea = primera_linea + "/" + directorio

        with open(log_dir, 'w') as archivo_escritura:
            archivo_escritura.writelines(primera_linea)

    except Exception as e:
        print(f"Error al leer el archivo: {e}")

#Función para conseguir el directorio actualizado 
def obtener_working_dir():

    log_dir = ssh_dict['log_dir']

    try:
        # Leer la primera línea del archivo y asignarla a una variable
        with open(log_dir, "r") as file:
            primera_linea = file.readline().strip()
        return os.path.normpath(primera_linea)
    except FileNotFoundError:
        print(f"El archivo '{log_dir}' no se encontró.")
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
    return None

def pwd_get_dir():
    
    log_dir = ssh_dict['log_dir']
    log_dir = os.path.normpath(ACTUAL_PATH +'/' + log_dir)

    try:
        # Leer la primera línea del archivo y asignarla a una variable
        with open(log_dir, "r") as file:
            primera_linea = file.readline().strip()

        if "/ssh/honeypot_files" in primera_linea: 
            pwd_xtra = primera_linea.split("/ssh/honeypot_files")[-1]
        return os.path.normpath(pwd_xtra)

    except Exception as e:
        print(f"Error al leer el archivo: {e}")

