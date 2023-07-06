import os
import paramiko
import socket
import sys
import threading
import subprocess

CWD = os.path.dirname(os.path.realpath(__file__))
HOSTKEY = paramiko.RSAKey(filename=os.path.join(CWD, 'id_rsa'))

LOG_FILE = './Server_Files/server_log.txt'
WORKING_DIRECTORY = './Server_Files/INFO_SERVER'
OUPUT_FILE = './Server_Files/output.txt'

# Funciones que creamos a parte de las de la clase servidor
def replace_prefix(output):

    replacement = '/root'

    part_before_INFO_SERVER = output.split("/INFO_SERVER/")[0]
    output = output.replace(part_before_INFO_SERVER, replacement)

    return output

# Leer usuarios y contraseñas validos
def parse_file(file_path):
    usernames = []
    passwords = []

    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split(':')
            if len(parts) >= 2:
                usernames.append(parts[0])
                passwords.append(parts[2])

    return usernames, passwords


#clase servidor con funciones de checkear el canal y el usuario y contraseña
class Server(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        if (username == 'user') and (password == 'pass'):
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED
    
    # def check_auth_password(self, username, password):
    # usernames, passwords = parse_file('ruta_del_archivo.txt')
    
    # if username in usernames and password in passwords:
    #     return paramiko.AUTH_SUCCESSFUL
    
    # return paramiko.AUTH_FAILED

    

if __name__ == '__main__':



    #ip y puerto donde se va a ejecutar el servidor
    server = '127.0.0.1'
    ssh_port = 22222
    try:
        #creamos socket tcp
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((server, ssh_port))
        sock.listen(100)
        print('[+] Listening for connection...')
        client, addr = sock.accept()
    except Exception as e:
        print('[-] Listen failed' + str(e))
        sys.exit(1)

    else:
        print(f'[+] Got a connection from ', addr)

    bhSession = paramiko.Transport(client)
    bhSession.add_server_key(HOSTKEY)
    server = Server()
    bhSession.start_server(server=server)

    #Espera a que el cliente abra un canal ssh
    chan = bhSession.accept(20)

    if chan is None:
        print('*** No Channel.')
        sys.exit(1)

    print('[+] Authenticated!')
    print(chan.recv(1024).decode())

    print('============================================')

    try:
        while True:
            print('Waiting for msg from Client ...')
            cmd_from_client = chan.recv(1024).decode()
            print('Mensaje recibido:', cmd_from_client, '\n')

            if cmd_from_client != '':

                subprocess.run(f'cd {WORKING_DIRECTORY} && {cmd_from_client} > ./../output.txt', shell=True)
                # output_path = WORKING_DIRECTORY + OUPUT_FILE

                # Guardar el mensaje en el archivo de registro
                with open(LOG_FILE, 'a') as log_file:
                    log_file.write(cmd_from_client + '\n')

                # Leer el archivo de salida y obtener su contenido
                with open(OUPUT_FILE, 'r') as file:
                    output = file.read()
                
                # Cambiar el PWD real por /root
                if cmd_from_client == 'pwd':
                    output = replace_prefix(output)

                output = output.encode()
                chan.send(output)


            # else:
            #     print('Cerrando el servidor')
            #     bhSession.close()
            #     break

            
    except KeyboardInterrupt:
        bhSession.close()