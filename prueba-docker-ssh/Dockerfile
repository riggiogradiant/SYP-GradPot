# Utiliza una imagen base que incluya un servidor SSH, como Ubuntu
FROM ubuntu:latest

# Actualiza el sistema e instala el servidor SSH
RUN apt-get update && \
    apt-get install -y openssh-server && \
    mkdir -p /run/sshd

# Copia el archivo de configuración SSH personalizado
COPY sshd_config /etc/ssh/sshd_config

# Agrega un usuario
RUN useradd -m -s /bin/bash riggio

# Establece la contraseña del usuario (¡Cambia "password" por una contraseña segura!)
RUN echo 'riggio:p' | chpasswd

# Expone el puerto SSH
EXPOSE 22

# Inicia el servidor SSH
CMD ["/usr/sbin/sshd", "-D"]
