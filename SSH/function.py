import subprocess

def replace_prefix(output):

    replacement = '/root'

    part_before_INFO_SERVER = output.split("/INFO_SERVER/")[0]
    output = output.replace(part_before_INFO_SERVER, replacement)

    return output


def execute_cmd(cmd_from_client):

    LOG_FILE = './Server_Files/server_log.txt'
    WORKING_DIRECTORY = './Server_Files/INFO_SERVER'
    OUPUT_FILE = './Server_Files/output.txt'

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
        print(output)