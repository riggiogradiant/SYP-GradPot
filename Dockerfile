FROM python:3

WORKDIR /app

# set environment variables
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip3 install --upgrade pip
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt

COPY ./HP /app

# WORKDIR /app/src/application/ssh

RUN apt-get update && apt-get install -y iptables openssh-server
RUN service ssh start
RUN chmod +x docker-start.sh
EXPOSE 2222

# Comando para ejecutar el archivo honeypot.py
# CMD ["python3", "honeypot.py", "-D"]
CMD ["./docker-start.sh"]
