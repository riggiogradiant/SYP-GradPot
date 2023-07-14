# import socket

# # Configuración del servidor
# host = '127.0.0.1'  # Dirección IP del servidor
# port = 8080  # Puerto para la conexión

# # Crear un socket TCP/IP
# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# # Vincular el socket al host y puerto especificados
# sock.bind((host, port))

# # Escuchar las conexiones entrantes (máximo de 1 conexión en espera)
# sock.listen(1)

# print('Servidor TCP escuchando en {}:{}'.format(host, port))

# while True:
#     # Esperar una conexión entrante
#     print('Esperando conexiones...')
#     client_sock, client_addr = sock.accept()
#     print('Conexión entrante desde {}:{}'.format(client_addr[0], client_addr[1]))

#     # Recibir datos del cliente
#     data = client_sock.recv(1024).decode('utf-8')
#     print('Datos recibidos:', data)

#     # Procesar los datos recibidos (opcional)
#     response = '¡Hola cliente! He recibido tus datos: {}'.format(data)

#     # Enviar la respuesta al cliente
#     client_sock.sendall(response.encode('utf-8'))
#     print('Respuesta enviada:', response)

#     # Cerrar la conexión con el cliente
#     client_sock.close()

import paramiko
import socket
import threading
import subprocess
import os

# Clase de servidor SSH
def run_command(command):
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        return output.decode('utf-8').strip()
    except subprocess.CalledProcessError as e:
        return 'Error al ejecutar el comando: {}'.format(e.output.decode('utf-8').strip())

class SSHServer(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()

    def check_auth_password(self, username, password):
        # Verificar las credenciales del cliente
        if username == 'user' and password == 'pass':
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_channel_shell_request(self, channel):
        self.event.set()
        return True

# Configuración del servidor SSH
host = '127.0.0.1'  # Dirección IP del servidor
port = 8080  # Puerto SSH
CWD = os.path.dirname(os.path.realpath(__file__))
HOSTKEY = paramiko.RSAKey(filename=os.path.join(CWD, 'id_rsa'))

# Crear un socket TCP/IP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Vincular el socket al host y puerto especificados
sock.bind((host, port))

# Escuchar las conexiones entrantes (máximo de 1 conexión en espera)
sock.listen(1)

print('Servidor SSH escuchando en {}:{}'.format(host, port))

# Esperar una conexión entrante
print('Esperando conexiones...')
client_sock, client_addr = sock.accept()
print('Conexión entrante desde {}:{}'.format(client_addr[0], client_addr[1]))

try:
    # Crear el servidor SSH
    ssh_server = SSHServer()

    # Configurar el transporte SSH
    transport = paramiko.Transport(client_sock)
    print('ANTES DEL HOSTKEY')
    transport.add_server_key(HOSTKEY)  # Agregar una clave SSH (opcional)
    print('DESPUES DEL HOSTKEY')
    transport.start_server(server=ssh_server)
    print('DESPUES DE INICIAR EL SERVER')

    # Esperar a que se establezca una sesión
    channel = transport.accept(10)
    print('SE CREÓ LA CONEXIÓN')
    print(channel)

    if channel is not None:
        print("Estoy dentro del channel not None")
        s_serv_eve = ssh_server.event.wait(10)
        print(s_serv_eve)  # Esperar hasta 10 segundos para la shell interactiva
        print("Se creó la shell interactiva")

        # Si se ha establecido la shell interactiva, redirigir la entrada/salida/err
        #if ssh_server.event.is_set():
        if s_serv_eve == 'True':
            channel.send('¡Bienvenido a la shell SSH!\r\n')
            channel.send('Ingrese comandos y presione Enter para ejecutarlos.\r\n')

            while True:
                command = channel.recv(1024).decode('utf-8').strip()
                if command == 'exit':
                    break
                # Ejecutar el comando y enviar la salida al cliente
                output = run_command(command)
                channel.send(output + '\r\n')

            channel.close()

except Exception as e:
    print('Error:', str(e))

finally:
    client_sock.close()
