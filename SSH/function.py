import subprocess
import os

def replace_prefix(output):

    replacement = '/root'

    part_before_INFO_SERVER = output.split("/INFO_SERVER/")[0]
    output = output.replace(part_before_INFO_SERVER, replacement)

    return output


def execute_cmd(cmd_from_client):

    LOG_FILE = './Server_Files/server_log.txt'
    WORKING_DIRECTORY = './Server_Files/INFO_SERVER'
    OUPUT_FILE = './Server_Files/output.txt'

    try:
        subprocess.run(f'cd {WORKING_DIRECTORY} && {cmd_from_client} > ./../output.txt', shell=True)

        # Guardar los logs en un archivo
        with open(LOG_FILE, 'a') as log_file:
            log_file.write(cmd_from_client + '\n')


        # Leer el archivo de salida y obtener su contenido
        with open(OUPUT_FILE, 'r') as file:
            output = file.read()

                # Cambiar el PWD real por /root
            if cmd_from_client == 'pwd':
                output = replace_prefix(output)

            #Con este print, imprimimos directamente en la terminal del cliente
    except subprocess.CalledProcessError as e:
        error_message = str(e.output.decode('utf-8')).strip()
        if error_message == "/bin/sh: 1: po: not found":
            output = 'None Command'
        else:
        # Si hay una excepción pero no es la específica que esperas, puedes manejarla de otra manera.
        # Por ejemplo, puedes relanzar la excepción con 'raise' para que se maneje en otro lugar.
            raise e

    print(output)

def cmd_cd(cmd_from_client):
    dir = cmd_from_client.split(" ")[1]
    # Obtén el directorio de trabajo actual del proceso principal
    current_directory = os.getcwd()
    
    WORKING_DIRECTORY = './Server_Files/INFO_SERVER/' + dir

    # Cambia el directorio de trabajo al directorio deseado
    os.chdir(WORKING_DIRECTORY)

    # Cambia el directorio de trabajo de vuelta al directorio original
    os.chdir(current_directory)
