# import socket
# import paramiko
# import threading

# # Diccionario con usuarios y contraseñas permitidos
# allowed_users = {
#     'myuser': 'pass',
# }

# class MySSHServer(paramiko.ServerInterface):
#     def __init__(self):
#         self.event = threading.Event()

#     def check_auth_password(self, username, password):
#         # Verifica si el usuario y la contraseña están en el diccionario de usuarios permitidos
#         if username in allowed_users and allowed_users[username] == password:
#             return paramiko.AUTH_SUCCESSFUL
#         return paramiko.AUTH_FAILED

# def start_ssh_server(port):
#     # Crea un socket TCP/IP
#     server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

#     # Enlaza el socket a una dirección y puerto
#     server_socket.bind(('127.0.0.1', port))

#     # Escucha las conexiones entrantes
#     server_socket.listen(1)
#     print(f"[*] Esperando conexiones SSH en el puerto {port}...")

#     while True:
#         # Acepta una nueva conexión
#         client_socket, address = server_socket.accept()
#         print(f"[*] Conexión SSH establecida desde {address[0]}:{address[1]}")

#         try:
#             # Crea un objeto de transporte SSH
#             print('[~] Antes de crear un objeto de transporte SSH')
#             transport = paramiko.Transport(client_socket)
#             print('[~] Después de crear un objeto de transporte SSH')

#             # Configura la autenticación usando la clase personalizada MySSHServer
#             print('[~] Antes de la autenticación')
#             ssh_server = MySSHServer()
#             transport.add_server_key(paramiko.RSAKey.generate(2048))
#             transport.set_subsystem_handler('sftp', paramiko.SFTPServer)
#             transport.start_server(server=ssh_server)
#             print('[~] Después de la autenticación')

#             # Acepta el canal de transporte
#             channel = transport.accept(20)
#             if channel is not None:
#                 msg = 'Hola desde el server'
#                 channel.send(msg.encode())

#                 while True:
#                     print('HooOooLa')

#             # Cierra el canal de transporte
#             # channel.close()

#         except paramiko.SSHException as e:
#             print(f"[-] Error en la conexión SSH: {str(e)}")

#         except Exception as ex:
#             print(f"[-] Error desconocido: {str(ex)}")

#         finally:
#             # Cierra el transporte
#             transport.close()
#             # Cierra el socket del cliente
#             client_socket.close()

# def main():
#     # Puerto en el que se ejecutará el servidor SSH
#     port = 2222

#     # Inicia el servidor SSH en el puerto especificado
#     start_ssh_server(port)

# if __name__ == "__main__":
#     main()

import socket
import paramiko
import threading
# Diccionario con usuarios y contraseñas permitidos
allowed_users = {
    'myuser': 'pass',
}

class MySSHServer(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()

    def check_auth_password(self, username, password):
        # Verifica si el usuario y la contraseña están en el diccionario de usuarios permitidos
        if username in allowed_users and allowed_users[username] == password:
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

def start_ssh_server(port):
    # Crea un socket TCP/IP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Enlaza el socket a una dirección y puerto
    server_socket.bind(('127.0.0.1', port))

    # Escucha las conexiones entrantes
    server_socket.listen(1)
    print(f"[*] Esperando conexiones SSH en el puerto {port}...")

    while True:
        # Acepta una nueva conexión
        client_socket, address = server_socket.accept()
        print(f"[*] Conexión SSH establecida desde {address[0]}:{address[1]}")

        try:
            # Crea un objeto de transporte SSH
            print('[~] Antes de crear un objeto de transporte SSH')
            transport = paramiko.Transport(client_socket)
            print('[~] Después de crear un objeto de transporte SSH')

            # Configura la autenticación usando la clase personalizada MySSHServer
            print('[~] Antes de la autenticación')
            ssh_server = MySSHServer()
            transport.add_server_key(paramiko.RSAKey.generate(2048))
            transport.set_subsystem_handler('sftp', paramiko.SFTPServer)
            transport.start_server(server=ssh_server)
            print('[~] Después de la autenticación')

            # Acepta el canal de transporte
            channel = transport.accept(20)
            if channel is not None:
                while True:
                    # Leer el comando ingresado por el cliente y responder con un mensaje
                    command = channel.recv(1024).decode().strip()
                    response = f'Ejecutando comando: {command}\r\n'
                    channel.send(response.encode())

        except paramiko.SSHException as e:
            print(f"[-] Error en la conexión SSH: {str(e)}")

        finally:
            # Cierra el canal de transporte
            if channel is not None:
                channel.close()

            # Cierra el transporte
            transport.close()
            # Cierra el socket del cliente
            client_socket.close()

def main():
    # Puerto en el que se ejecutará el servidor SSH
    port = 2222

    # Inicia el servidor SSH en el puerto especificado
    start_ssh_server(port)

if __name__ == "__main__":
    main()
