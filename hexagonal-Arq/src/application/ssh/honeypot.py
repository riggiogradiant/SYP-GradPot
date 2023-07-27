import threading
import socket
import sys
import os
import traceback
import logging
import paramiko
import subprocess
import random
import ssh_functions

from ..configuration.load_config import cargar_seccion_ssh



HOST_KEY = paramiko.RSAKey(filename='server.key')
SSH_BANNER = "SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.1"

ACTUAL_PATH = os.getcwd()
CONFIG_FILE = os.path.join(ACTUAL_PATH, '../../../', 'config.json')
CONFIG_FILE = os.path.normpath(CONFIG_FILE)

ssh_detection = cargar_seccion_ssh(CONFIG_FILE)




UP_KEY = '\x1b[A'.encode()
DOWN_KEY = '\x1b[B'.encode()
RIGHT_KEY = '\x1b[C'.encode()
LEFT_KEY = '\x1b[D'.encode()
BACK_KEY = '\x7f'.encode()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    filename='../../infrastructure/logs/ssh_honeypot.log')

# Devuelve un diccionario de los usuarios y de las contraseñas
def get_user_pass(file_path):
    user_pass_dict = {}  # Crear un diccionario vacío

    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split(':')
            if len(parts) >= 3:
                username = parts[0]
                password = parts[2]
                user_pass_dict[username] = password

    return user_pass_dict


# Función para sacar info del json en función a su etiqueta


USERDB_FILE = ssh_functions.valor_json_etiqueta("userdb")
HP_WORKING_DIR = ACTUAL_PATH + ssh_functions.valor_json_etiqueta("working_dir")



class BasicSshHoneypot(paramiko.ServerInterface):

    client_ip = None

    def __init__(self, client_ip):
        self.client_ip = client_ip
        self.event = threading.Event()

    def check_channel_request(self, kind, chanid):
        logging.info('client called check_channel_request ({}): {}'.format(
                    self.client_ip, kind))
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED

    def get_allowed_auths(self, username):
        logging.info('client called get_allowed_auths ({}) with username {}'.format(
                    self.client_ip, username))
        return "password"  # Enable password-based authentication

    def check_auth_password(self, username, password):
        # Verify the received username and password against the allowed users' credentials.

        ALLOWED_USERS = get_user_pass(USERDB_FILE)

        if username in ALLOWED_USERS and password == ALLOWED_USERS[username]:
            logging.info('New client authenticated with password ({}): username: {}'.format(
                self.client_ip, username))
            logging.info('New client with ID: ' + str(random.randint(100000, 999999)))
            return paramiko.AUTH_SUCCESSFUL
        else:
            logging.info('Failed password authentication ({}): username: {}'.format(
                self.client_ip, username))
            return paramiko.AUTH_FAILED

    def check_channel_shell_request(self, channel):
        self.event.set()
        return True

    def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes):
        return True

    def check_channel_exec_request(self, channel, command):
        command_text = str(command.decode("utf-8"))

        logging.info('client sent command via check_channel_exec_request ({}): {}'.format(
                    self.client_ip, command))
        return True


def handle_connection(client, addr):

    client_ip = addr[0]
    logging.info('New connection from: {}'.format(client_ip))

    try:
        transport = paramiko.Transport(client)
        transport.add_server_key(HOST_KEY)
        transport.local_version = SSH_BANNER # Change banner to appear more convincing
        server = BasicSshHoneypot(client_ip)
        try:
            transport.start_server(server=server)

        except paramiko.SSHException:
            print('*** SSH negotiation failed.')
            raise Exception("SSH negotiation failed")

        # wait for auth
        chan = transport.accept(100)
        if chan is None:
            print('*** No channel (from '+client_ip+').')
            raise Exception("No channel")
        
        chan.settimeout(1000)

        if transport.remote_mac != '':
            logging.info('Client mac ({}): {}'.format(client_ip, transport.remote_mac))

        if transport.remote_compression != '':
            logging.info('Client compression ({}): {}'.format(client_ip, transport.remote_compression))

        if transport.remote_version != '':
            logging.info('Client SSH version ({}): {}'.format(client_ip, transport.remote_version))
            
        if transport.remote_cipher != '':
            logging.info('Client SSH cipher ({}): {}'.format(client_ip, transport.remote_cipher))

        server.event.wait(100)
        if not server.event.is_set():
            logging.info('** Client ({}): never asked for a shell'.format(client_ip))
            raise Exception("No shell request")
     
        try:

            log_file = os.path.join("../../infrastructure/logs", "dir.log")
            with open(log_file, "w") as file:
                file.write(HP_WORKING_DIR)

            chan.send("Welcome to Ubuntu 18.04.4 LTS (GNU/Linux 4.15.0-128-generic x86_64)\r\n\r\n")
            run = True
            while run:
                chan.send("$ ")
                command = ""
                while not command.endswith("\r"):
                    transport = chan.recv(1024)
                    
                    # Echo input to pseudo-simulate a basic terminal
                    if (
                        transport != UP_KEY
                        and transport != DOWN_KEY
                        and transport != LEFT_KEY
                        and transport != RIGHT_KEY
                        and transport != BACK_KEY
                    ):
                        chan.send(transport)
                        command += transport.decode("utf-8")
                
                chan.send("\r\n")
                command = command.rstrip()
                print(client_ip+"- received:", command)
                logging.info('Command received ({}): {}'.format(client_ip, command))

                if command == "exit":
                    # As we don't have the settings module, just printing the log message.
                    print("Connection closed (via exit command): " + client_ip)
                    run = False

                else:
                    # EJECUTA EL COMANDO
                    args = ["python3", "../../../hp_main.py", command, client_ip]
                    output = subprocess.check_output(args)
                    chan.send(output.decode()+"\n")


        except Exception as err:
            print('!!! Exception: {}: {}'.format(err.__class__, err))
            try:
                transport.close()
            except Exception:
                pass

        chan.close()

    except Exception as err:
        print('!!! Exception: {}: {}'.format(err.__class__, err))
        try:
            transport.close()
        except Exception:
            pass


def start_server(port, bind):
    """Init and run the ssh server"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((bind, port))
    except Exception as err:
        print('*** Bind failed: {}'.format(err))
        traceback.print_exc()
        sys.exit(1)

    threads = []
    while True:
        try:
            sock.listen(100)
            # print('Listening for connection ...')
            client, addr = sock.accept()
        except Exception as err:
            print('*** Listen/accept failed: {}'.format(err))
            traceback.print_exc()
        new_thread = threading.Thread(target=handle_connection, args=(client, addr))
        new_thread.start()
        threads.append(new_thread)


if __name__ == "__main__":

    

    host = ssh_functions.valor_json_etiqueta("host")
    port = ssh_functions.valor_json_etiqueta("port")
    print('Listening for connection ...')
    start_server(port, host)
    
