import socket
import paramiko

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

            # Configura la autenticación (puedes personalizarlo según tus necesidades)
            print('[~] Antes de la autenticación')

            transport.add_server_key(paramiko.RSAKey.generate(2048))
            transport.set_subsystem_handler('sftp', paramiko.SFTPServer)

            print('[~] Después de la autenticación')

            # Inicia la sesión SSH
            print('[~] Antes de iniciar el servidor')
            transport.start_server(server=paramiko.ServerInterface())
            print('[~] Después de iniciar el servidor')

            channel = transport.accept(20)
            msg = 'Hola desde el server'
            channel.send(msg.encode())
            # Envía un mensaje al cliente
            # message = "¡Hola, cliente SSH!"
            # transport.send(message.encode())
            while True:
                print('HooOooLa')

        except paramiko.SSHException as e:
            print(f"[-] Error en la conexión SSH: {str(e)}")

        finally:
            # Cierra la conexión
            channel.close()
            transport.close()
            client_socket.close()

def main():
    # Puerto en el que se ejecutará el servidor SSH
    port = 2222

    # Inicia el servidor SSH en el puerto especificado
    start_ssh_server(port)

if __name__ == "__main__":
    main()
