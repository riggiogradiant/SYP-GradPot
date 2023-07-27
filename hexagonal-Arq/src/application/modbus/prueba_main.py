import subprocess

output = subprocess.check_output(["python3", "../../../hp_main.py", 'hola'])
print(output.decode())
