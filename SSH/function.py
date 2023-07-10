import subprocess
import os
import datetime

#PATHS RELATIVOS
LOG_FILE = os.getcwd()
LOG_FILE = LOG_FILE + '/Server_Files/server_log.txt'

OUTPUT_FILE = os.getcwd()
OUTPUT_FILE = OUTPUT_FILE + '/Server_Files/output.txt'

# BASE_DIRECTORY = os.getcwd()
# BASE_DIRECTORY = BASE_DIRECTORY +'/Server_Files/INFO_SERVER'

def replace_prefix(output, dir):
    replacement = '/root'
    if dir is not None:
        output = replacement + '/' + dir
    else:
        output = replacement
    return output


# Retorna True si el working dir es valido y false si no lo es
def valid_path(Base_Dir, Working_Dir):
    count1 = Base_Dir.count('/')
    count2 = Working_Dir.count('/')
    
    return count1 <= count2

def dir_to_change(log_file):
    cd_commands = []
    authenticated_found = False

    with open(log_file, 'r') as file:
        for line in file:
            if 'INFO - [+] Authenticated!' in line:
                authenticated_found = True
                cd_commands.clear()  # Limpiar la lista de comandos 'cd' anteriores
                continue

            if authenticated_found and '- CMD - cd' in line:
                command_parts = line.split('- CMD - cd')
                if len(command_parts) == 2:
                    directory = command_parts[1].strip()
                    cd_commands.append(directory)

    if cd_commands:
        directories = '/'.join(cd_commands)
        print('DIR to CHANGE FUNCTION. DIRs:', directories)
        return directories

    return None



# Función de ejecución de los comandos
def execute_cmd(cmd_from_client):

    WORKING_DIRECTORY = os.getcwd()
    WORKING_DIRECTORY = WORKING_DIRECTORY +'/Server_Files/INFO_SERVER'

    #Guarda el comando recibido con su timestamp en el LOG-FILE
    timestamp = timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S,%f")[:-3]
    log_to_enter= f"{timestamp} - CMD - {cmd_from_client}\n"

    with open(LOG_FILE, 'a') as log_file:
        log_file.write(log_to_enter)

    WORKING_DIRECTORY, directory = dir_dealer(cmd_from_client)
    os.chdir(WORKING_DIRECTORY)
    print('DIRECTORIO EN EL QUE SE TRABAJA: ' + WORKING_DIRECTORY)

    if cmd_from_client.startswith("vi"):
        print('El cmd empieza por VI')
        subprocess.run(['vi', OUTPUT_FILE])


        print('Despues del subprovess')

    else:
        subprocess.run(f'{cmd_from_client} > {OUTPUT_FILE}', shell=True)


    with open(OUTPUT_FILE, 'r') as file:
        output = file.read()

    if cmd_from_client == 'pwd':
        output = replace_prefix(output, directory)

    print(output)



# Función que nos devuelve el directorio completo sobre el que estamos trabajando
def dir_dealer(cmd_from_client):
    WORKING_DIRECTORY = os.getcwd()
    WORKING_DIRECTORY = WORKING_DIRECTORY +'/Server_Files/INFO_SERVER'
    
    directory = dir_to_change(LOG_FILE)

    print(directory)

    print('-+-+-+-+-+-CMD_FROM_CLIENT:' +cmd_from_client)

    if directory != None:
        #print('Directory dentro del cd_dealer' + directory)
        WORKING_DIRECTORY = WORKING_DIRECTORY +'/'+ directory

        #print('Directorio antes de normalizar: '+ WORKING_DIRECTORY)

        #Con esto normalizamos el path y nos deshacemos de un path redundate
        WORKING_DIRECTORY = os.path.normpath(WORKING_DIRECTORY)
        #print('Directorio despues de normalizar: '+ WORKING_DIRECTORY)

        # Con esto conseguimos el dir ya normalizado
        try:
            directory = WORKING_DIRECTORY.split("/INFO_SERVER/")[1]
        except IndexError:
            directory = None

    return WORKING_DIRECTORY, directory














#FUNCIONES SIN USO:

def detect_cd():

    with open(LOG_FILE, 'r') as archivo:
        lineas = archivo.readlines()

    penultima_linea = lineas[-1].strip()
    print('---------PENULTIMA LÍNEA DEL DETECT_CD:' + penultima_linea)

    if penultima_linea.startswith('cd'):
        print('True CD')
        x =True
    elif penultima_linea == 'cd ..':
        print('cd ..')
        x = 'cd ..'
    else:
        print('False CD')
        x = False
    return x

def cd_dealer(cmd_from_client):

    WORKING_DIRECTORY = os.getcwd()
    WORKING_DIRECTORY = WORKING_DIRECTORY +'/Server_Files/INFO_SERVER'

    # directory = dir_to_change(LOG_FILE)
    # if directory != None:
    #     print('Directory dentro del cd_dealer' + directory)
    #     WORKING_DIRECTORY = WORKING_DIRECTORY +'/'+ directory

    # #print('DIRECTORIO EN EL QUE ESTOY DESDE EL CD DEALER: '+ WORKING_DIRECTORY)
    # print('COMANDO RECIBIDO: '+ cmd_from_client)
    # print('Anstes del cd ..')
    # if detect_cd() == 'cd ..':

    #     print('DENTRO DEL CD.. WORKIND DIRECTORY:' + WORKING_DIRECTORY)

    #     last_slash = WORKING_DIRECTORY.rfind("/")
    #     WORKING_DIRECTORY = WORKING_DIRECTORY[:last_slash]

    #     print('DENTRO DEL CD.. WORKIND DIRECTORY:' + WORKING_DIRECTORY)
    # print('Despues del cd ..')

    return WORKING_DIRECTORY

def cmd_cd(cmd_from_client):
    print('DIR Changed')
    with open(LOG_FILE, 'a') as log_file:
        log_file.write(cmd_from_client + '\n')