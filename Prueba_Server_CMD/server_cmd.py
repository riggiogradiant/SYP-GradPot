import paramiko
import threading
import sys

# Definir la configuración del servidor SSH
HOST = '127.0.0.1'
PORT = 22222
USERNAME = 'user'
PASSWORD = 'pass'

# Definir la clase del manejador del servidor SSH
class SSHServer(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()

    def check_auth_password(self, username, password):
        # Verificar el nombre de usuario y la contraseña
        if (username == USERNAME) and (password == PASSWORD):
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

    def check_channel_request(self, kind, chanid):
        # Permitir todas las solicitudes de canal
        return paramiko.OPEN_SUCCEEDED

    def check_channel_shell_request(self, channel):
        # Permitir una solicitud de shell
        return True

# Crear el servidor SSH
server = paramiko.Transport((HOST, PORT))
server.add_server_key(paramiko.RSAKey.generate(2048))
ssh_server = SSHServer()

try:
    server.start_server(server=ssh_server)
    print('Servidor SSH iniciado.')

    # Esperar por una conexión del cliente
    client = server.accept(20)
    if client is None:
        print('Tiempo de espera de conexión excedido. Saliendo.')
        server.close()
        sys.exit(1)

    print('Cliente conectado.')

    # Abrir un canal SSH
    channel = client.open_session()

    # Conectar el canal a una terminal interactiva
    channel.get_pty()
    channel.invoke_shell()

    # Leer comandos del cliente y enviar respuestas
    while True:
        if channel.recv_ready():
            data = channel.recv(1024)
            # Procesar los comandos del cliente y enviar respuestas
            # Aquí puedes escribir tu lógica personalizada
            response = 'Respuesta del servidor\n'
            channel.send(response)

except Exception as e:
    print('Error: ', str(e))
    server.close()
    sys.exit(1)
