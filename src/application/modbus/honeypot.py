import subprocess
import time
import logging
from modbus_functions import get_path_from_config_converted


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    filename = get_path_from_config_converted('log_file')
)

print("Listening for Modbus connections ...")

#Hacemos el sleep para ver que concurrentemente puede lidiar tanto con ssh como con Modbus
time.sleep(5)
output = subprocess.check_output(["python3", "../../../hp_main.py", 'hola'])
print(output.decode())
logging.info(output.decode())
