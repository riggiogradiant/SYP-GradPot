import subprocess

output = subprocess.check_output(["python3", "../main.py", 'hola'])
print(output.decode())