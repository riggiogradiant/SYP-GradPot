#!/bin/bash

# Redirige el tráfico del puerto 22 al puerto 2222
sudo iptables -A PREROUTING -t nat -p tcp --dport 22 -j REDIRECT --to-port 2222

# Ejecuta el script honeypot.sh de Python 3 ubicado en src/application/ssh/
python3 src/application/ssh/honeypot.py
