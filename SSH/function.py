import subprocess
import os

LOG_FILE = os.path.abspath('/home/criggio/OWN_HONEYPOT/SSH/Server_Files/server_log.txt')
OUTPUT_FILE	 = os.path.abspath('/home/criggio/OWN_HONEYPOT/SSH/Server_Files/output.txt')

def replace_prefix(output, dir):
    replacement = '/root'
    if dir is not None:
        output = replacement + '/' + dir
    else:
        output = replacement
    return output

def cmd_cd(cmd_from_client):
    print('DIR Changed')
    with open(LOG_FILE, 'a') as log_file:
        log_file.write(cmd_from_client + '\n')


# Con esta funcion registramos todos los comandos cd despues de la ultima autenticación
def dir_to_change(log_file):
    print('DENTRO DEL DIR TO CHANGE')
    cd_commands = []
    authenticated_found = False

    with open(log_file, 'r') as file:
        for line in file:
            if 'INFO - [+] Authenticated!' in line:
                authenticated_found = True
                cd_commands.clear()  # Limpiar la lista de comandos 'cd' anteriores
                continue

            if authenticated_found and line.strip().startswith('cd'):
                cd_commands.append(line.strip())

    if cd_commands:
        last_cd_command = cd_commands[-1]
        directory = last_cd_command[3:].strip()  # Obtener el directorio después de 'cd'
        print('DIR to CHANGE FUNCTION. DIR:' + directory)
        return directory
    
    return None


# Función para ejecutar comandos que no sean ni cd ni pwd
def execute_cmd(cmd_from_client):
    WORKING_DIRECTORY = os.path.abspath('/home/criggio/OWN_HONEYPOT/SSH/Server_Files/INFO_SERVER')
    print('DENTRO DEL EXECUTE ANTES DEL DIR_TO_CHANGE')
    directory = dir_to_change(LOG_FILE)
    print('DENTRO DEL EXECUTE DESPUES DEL DIR_TO_CHANGE')

    if directory!=None:
        print('DIR TO CHANGE DENTRO DEL EXECUTE:' + directory)
        os.chdir(WORKING_DIRECTORY + '/' + directory)
    elif directory == None:
        os.chdir(WORKING_DIRECTORY)
    print('DIRECTORIO EN EL QUE SE TRABAJA: ' + WORKING_DIRECTORY)

    subprocess.run(f'{cmd_from_client} > {OUTPUT_FILE}', shell=True)

    with open(LOG_FILE, 'a') as log_file:
        log_file.write(cmd_from_client + '\n')

    with open(OUTPUT_FILE, 'r') as file:
        output = file.read()

    if cmd_from_client == 'pwd':
        output = replace_prefix(output, directory)

    print(output)

#Función para lidiar con las peticiones cd
def cd_dealer(cmd_from_client):
    WORKING_DIRECTORY = os.path.abspath('/home/criggio/OWN_HONEYPOT/SSH/Server_Files/INFO_SERVER')
    print('DENTRO DEL CD DEALER')

    with open(LOG_FILE, 'a') as log_file:
        log_file.write(cmd_from_client + '\n')

    split_cmd = cmd_from_client.split(" ")
    directory = split_cmd[1]

    WORKING_DIRECTORY = WORKING_DIRECTORY + '/' + directory

    print(WORKING_DIRECTORY)
