FROM python:3

WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1

#Para que se imprima el output en tiempo real
ENV PYTHONUNBUFFERED 1


# install dependencies
RUN pip3 install --upgrade pip
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt

COPY .  /app

WORKDIR /app/src/application/ssh
EXPOSE 2222

# Comando para ejecutar el archivo honeypot.py
# CMD ["python3", "honeypot.py", "-D"]
CMD ["python3", "honeypot.py"]
