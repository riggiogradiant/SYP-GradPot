import paramiko

def ssh_connect(ip, port, user, passwd):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, port=port, username=user, password=passwd)
    print('Connected to the SSH server.')

    # Abrir un canal SSH
    channel = client.get_transport().open_session()
    channel.send('Client succesfully connected')
    print('============================================')
    
    while True:
        msg_send = input('Enter command or <CR> to exit: ')
        if msg_send == '':
            break
        channel.send(msg_send)
        output = channel.recv(1024).decode()
        print('---MSG RECEIVED---')
        print(output, '\n')

    # Cerrar el canal y la conexión
    channel.close()
    client.close()

#main
if __name__ == '__main__':
    import getpass
    user = input('Username: ')
    
    #getpass: para no ver la contraseña cuando se escribe
    password = getpass.getpass()

    #puerto e ip en el que está configurado el server.py
    ip = input('Enter server IP: ') or '127.0.0.1'
    port = input('Enter port or <CR>: ') or 22222
    ssh_connect(ip, port, user, password)