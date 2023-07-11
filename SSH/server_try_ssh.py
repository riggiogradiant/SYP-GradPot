# import os
# import paramiko
# import socket
# import sys
# import threading
# import subprocess
# import random
# import logging

# # Configurar el registro
# log_file = './Server_Files/server_log.txt'
# logging.basicConfig(filename=log_file, level=logging.INFO,
#                     format='%(asctime)s - %(levelname)s - %(message)s')

# CWD = os.path.dirname(os.path.realpath(__file__))
# HOSTKEY = paramiko.RSAKey(filename=os.path.join(CWD, 'id_rsa'))

# # Leer usuarios y contraseñas validos
# def parse_file(file_path):
#     usernames = []
#     passwords = []

#     with open(file_path, 'r') as file:
#         for line in file:
#             parts = line.strip().split(':')
#             if len(parts) >= 2:
#                 usernames.append(parts[0])
#                 passwords.append(parts[2])

#     return usernames, passwords


# #clase servidor con funciones de checkear el canal y el usuario y contraseña
# class Server(paramiko.ServerInterface):
#     def __init__(self):
#         self.event = threading.Event()

#     def check_channel_request(self, kind, chanid):
#         if kind == 'session':
#             return paramiko.OPEN_SUCCEEDED
#         return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED


#     def check_auth_password(self, username, password):
#         usernames, passwords = parse_file('./Server_Files/INFO_SERVER/etc/userdb.txt')

#         if username in usernames and password in passwords:
#             if usernames.index(username) == passwords.index(password):
#                 # Registro de información (info log)

#                 #Generamos un nº random de 6 dígitos para identificar cada conexión
#                 connection_ID = random.randint(100000, 999999)

#                 logging.info("Succesfull Login - User: %s - Password: %s - ID: %s" , username, password, connection_ID)
#                 return paramiko.AUTH_SUCCESSFUL

#         # Registro de información (info log)
#         logging.info("Failed Login - User: %s - Password: %s", username, password)
#         return paramiko.AUTH_FAILED

#     # def check_channel_request(self, kind, chanid):
#     #     if kind == 'session':
#     #         if chanid == 0:
#     #             # Acciones específicas para el canal 0 (solicitud de PTY)
#     #             return paramiko.OPEN_SUCCEEDED
#     #     return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED


# if __name__ == '__main__':

#     #ip y puerto donde se va a ejecutar el servidor
#     server = '127.0.0.1'
#     ssh_port = 22222
#     try:
#         #creamos socket tcp
#         sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#         sock.bind((server, ssh_port))
#         sock.listen(100)
#         print('[+] Listening for connection...')
#         logging.info('[+] Listening for connection...')
#         client, addr = sock.accept()
#     except Exception as e:
#         print('[-] Listen failed' + str(e))
#         sys.exit(1)

#     else:
#         print(f'[+] Got a connection from ', addr)
#         logging.info(f'[+] Got a connection from {addr}')

# #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#     # bhSession = paramiko.Transport(client)
#     #  #####
#     # bhSession.set_gss_host(socket.getfqdn(""))
#     # bhSession.load_server_moduli()
#     #  #####
#     # bhSession.add_server_key(HOSTKEY)
#     # #####
#     # bhSession.set_subsystem_handler("sftp", paramiko.SFTPServer)
#     # #####
#     # server = Server()
#     # bhSession.start_server(server=server)

#     # #Espera a que el cliente abra un canal ssh
#     # chan = bhSession.accept(20)
#     # try:
#     #     chan.get_pty()
#     #     print('DESPUES DEL GET-PTY')
#     # except paramiko.SSHException as e:
#     #     print("Error al obtener el PTY:", str(e))



#     bhSession = paramiko.Transport(client)
#     bhSession.set_gss_host(socket.getfqdn(""))
#     bhSession.load_server_moduli()
#     bhSession.add_server_key(HOSTKEY)
#     bhSession.set_subsystem_handler("sftp", paramiko.SFTPServer)
#     server = Server()
#     bhSession.start_server(server=server)

#     # Espera a que el cliente abra un canal ssh
# # Espera a que el cliente abra un canal ssh

#     chan = bhSession.accept(20)

#     # if chan.get_id() == 0:
#     #     try:
#     #         print('++++++++++++++DENTRO DEL GETPTY+++++++++++++++')
#     #         chan.get_pty()
#     #         print('DESPUES DEL GET-PTY')
#     #     except paramiko.SSHException as e:
#     #         print("Error al obtener el PTY:", str(e))



# #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#     if chan is None:
#         print('*** No Channel.')
#         logging.info('*** No Channel.')
#         sys.exit(1)



#     print('[+] Authenticated!')
#     print(chan.recv(1024).decode())
#     logging.info('[+] Authenticated!')

#     # Abrir un canal de sesión
#     chan = bhSession.open_channel('session')

#     chan.get_pty()
#     chan.invoke_shell()


#     print('============================================')

#     try:
#         while True:
#             print('Waiting for msg from Client ...')
#             cmd_from_client = chan.recv(1024).decode()
#             print('Mensaje recibido:', cmd_from_client, '\n')

#         #if cmd_from_client != '':
#             # Envíamos el cmd al main y el se encarga de devolver lo que haya que enviar al cliente
#             output = subprocess.check_output(["python3", "../main.py", cmd_from_client])
#             output = output.decode().strip()
#             output = output.encode()
#             chan.send(output)
#         #else:
#             # print('Cerrando el servidor')
#             # bhSession.close()
#             # break


#     except KeyboardInterrupt:
#         bhSession.close()



import os
import paramiko
import socket
import sys
import threading
import subprocess
import random
import logging

# Configurar el registro
log_file = './Server_Files/server_log.txt'
logging.basicConfig(filename=log_file, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

CWD = os.path.dirname(os.path.realpath(__file__))
HOSTKEY = paramiko.RSAKey(filename=os.path.join(CWD, 'id_rsa'))

# Leer usuarios y contraseñas válidos
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


# Clase servidor con funciones para verificar el canal y el usuario y contraseña
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
                # Registro de información (info log)
                # Generamos un nº random de 6 dígitos para identificar cada conexión
                connection_ID = random.randint(100000, 999999)
                logging.info("Succesfull Login - User: %s - Password: %s - ID: %s", username, password, connection_ID)
                return paramiko.AUTH_SUCCESSFUL

        # Registro de información (info log)
        logging.info("Failed Login - User: %s - Password: %s", username, password)
        return paramiko.AUTH_FAILED


if __name__ == '__main__':
    # IP y puerto donde se va a ejecutar el servidor
    server = '127.0.0.1'
    ssh_port = 22222
    try:
        # Creamos socket TCP
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

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    #Establecer la Session
    bhSession = paramiko.Transport(client)
    bhSession.set_gss_host(socket.getfqdn(""))
    bhSession.load_server_moduli()
    bhSession.add_server_key(HOSTKEY)
    bhSession.set_subsystem_handler("sftp", paramiko.SFTPServer)
    server = Server()
    bhSession.start_server(server=server)

    # Espera que el cliene acepte la sesion y devuelve un canal del tipo session
    chan = bhSession.accept(20)
    chan = bhSession.open_channel('session')
    
    print('Canal del tipo session abierto')

    if chan is None:
        print('*** No Channel.')
        logging.info('*** No Channel.')
        sys.exit(1)

    print('[+] Authenticated!')
    print(chan.recv(1024).decode())
    logging.info('[+] Authenticated!')

    # Abre el canal que se creó al establecer la sesion
    # chan = bhSession.open_channel('session')
    
    # print('Canal del tipo session abierto')

    chan.get_pty()
    chan.invoke_shell()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    print('============================================')

    try:
        while True:
            print('Waiting for message from Client ...')
            cmd_from_client = chan.recv(1024).decode()
            print('Mensaje recibido:', cmd_from_client, '\n')

            # Send the command to the main script, which will handle the response to send back to the client
            output = subprocess.check_output(["python3", "../main.py", cmd_from_client])
            output = output.decode().strip()
            output = output.encode()
            chan.send(output)

    except KeyboardInterrupt:
        bhSession.close()