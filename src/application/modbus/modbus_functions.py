import os 
import sys

ACTUAL_PATH = os.getcwd() # este tambien es el config file path
CONFIG_FILE = os.path.join(ACTUAL_PATH,"../../../", "config.json")
CONFIG_FILE = os.path.normpath(CONFIG_FILE)


def get_path_from_config_converted(label):

    src_path = os.path.normpath(os.path.join(ACTUAL_PATH, '..', '..'))
    sys.path.append(src_path)
    from application.configuration.load_config import cargar_seccion_modbus
    modbus_dict = cargar_seccion_modbus(CONFIG_FILE)
    
    if label in modbus_dict:
        path_from_config = modbus_dict[label]

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