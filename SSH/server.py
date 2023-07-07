import os
import paramiko
import socket
import sys
import threading
import subprocess

import logging

# Configurar el registro
log_file = './Server_Files/server_log.txt'
logging.basicConfig(filename=log_file, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

CWD = os.path.dirname(os.path.realpath(__file__))
HOSTKEY = paramiko.RSAKey(filename=os.path.join(CWD, 'id_rsa'))

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
        usernames, passwords = parse_file('./Server_Files/INFO_SERVER/etc/userdb.txt')
    
        if username in usernames and password in passwords:
            if usernames.index(username) == passwords.index(password):
                return paramiko.AUTH_SUCCESSFUL

        return paramiko.AUTH_FAILED

    

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
        logging.info('[+] Listening for connection...')
        client, addr = sock.accept()
    except Exception as e:
        print('[-] Listen failed' + str(e))
        sys.exit(1)

    else:
        print(f'[+] Got a connection from ', addr)
        logging.info(f'[+] Got a connection from {addr}')

    bhSession = paramiko.Transport(client)
    bhSession.add_server_key(HOSTKEY)
    server = Server()
    bhSession.start_server(server=server)

    #Espera a que el cliente abra un canal ssh
    chan = bhSession.accept(20)

    if chan is None:
        print('*** No Channel.')
        logging.info('*** No Channel.')
        sys.exit(1)

    print('[+] Authenticated!')
    print(chan.recv(1024).decode())

    logging.info('[+] Authenticated!')
    

    print('============================================')

    try:
        while True:
            print('Waiting for msg from Client ...')
            cmd_from_client = chan.recv(1024).decode()
            print('Mensaje recibido:', cmd_from_client, '\n')

            if cmd_from_client != '':

                # Envíamos el cmd al main y el se encarga de devolver lo que haya que enviar al cliente
                output = subprocess.check_output(["python3", "../main.py", cmd_from_client])
                output = output.decode().strip()

                output = output.encode()
                chan.send(output)


            else:
                print('Cerrando el servidor')
                bhSession.close()
                break

            
    except KeyboardInterrupt:
        bhSession.close()

