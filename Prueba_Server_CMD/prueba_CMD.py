import paramiko

hostname = '127.0.0.1'
port = 22
user = 'criggio'
pwd = '123456'

try:
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname, port= port, username= user, password=pwd)
    while True:
        try:
            cmd = input("$> ")
            if cmd == "exit": break
            stdin, stdout, stderr = client.exec_command(cmd)
            print(stdout.read().decode())
        except KeyboardInterrupt:
            break
    client.close()
except Exception as err:
    print(str(err))