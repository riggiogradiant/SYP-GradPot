import threading
import socket
import sys
import os
import traceback
import logging
import paramiko
import subprocess
import random


HOST_KEY = paramiko.RSAKey(filename='server.key')

#Variable Global para implementar el whoami con los distintos usuarios
USERNAME_SESSION = ""



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
 
UP_KEY = '\x1b[A'.encode()
DOWN_KEY = '\x1b[B'.encode()
RIGHT_KEY = '\x1b[C'.encode()
LEFT_KEY = '\x1b[D'.encode()
BACK_KEY = '\x7f'.encode()

def get_path_from_config_converted(label):

    ssh_dict = cargar_seccion_ssh(CONFIG_FILE)
    
    if label in ssh_dict:
        path_from_config = ssh_dict[label]

        #comprobamos si es de tipo int
        if isinstance(path_from_config,int):
            path_convertido = path_from_config
        #comprobamos si es un path
        elif '/' in path_from_config:
            path_inicial = ACTUAL_PATH.split("src/")[0]
            path_convertido = str(path_inicial) + path_from_config
        # este caso es si es una string
        else: 
            path_convertido = path_from_config
          
    else:
        raise KeyError(f"'{label}' no encontrado en la configuración SSH.")

    return path_convertido

SSH_BANNER = get_path_from_config_converted('ssh_banner')
USERDB_FILE = get_path_from_config_converted('userdb')
HP_WORKING_DIR = get_path_from_config_converted('working_dir')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    filename = get_path_from_config_converted('log_file')
)

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
        global USERNAME_SESSION
        ALLOWED_USERS = get_user_pass(USERDB_FILE)

        if username in ALLOWED_USERS and password == ALLOWED_USERS[username]:
            logging.info(' New client authenticated with password ({}): username: {}'.format(
                self.client_ip, username))
            USERNAME_SESSION = username
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
    logging.info('[{}] New connection from: {}'.format(client.getpeername()[1], client_ip))

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
            log_file =  get_path_from_config_converted('log_dir')
            with open(log_file, "w") as file:
                file.write(HP_WORKING_DIR)

            welcome_msg = get_path_from_config_converted('welcome_msg_client')
            chan.send(welcome_msg +"\r\n\r\n")
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
                logging.info('[{}] [{}] Command received ({}): {}'.format(client.getpeername()[1], USERNAME_SESSION ,client_ip, command))

                if command == "exit":
                    print("Connection closed (via exit command): " + client_ip)
                    run = False

                else:
                    args = ["python3", "../../../hp_main.py", command, client_ip, USERNAME_SESSION]
                    output = subprocess.check_output(args)
                    chan.send(output.decode()+"\r\n")


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
            client, addr = sock.accept()
        except Exception as err:
            print('*** Listen/accept failed: {}'.format(err))
            traceback.print_exc()
        
        new_thread = threading.Thread(target=handle_connection, args=(client, addr))
        new_thread.start()
        threads.append(new_thread)

    
if __name__ == "__main__":

    host = get_path_from_config_converted('host')
    port = get_path_from_config_converted('port')
    print('Listening for connection ...')
    start_server(port, host)
    
