FROM python:3

WORKDIR /app/SYP-GradPot

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1

#Para que se imprima el output en tiempo real
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip3 install --upgrade pip
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt

COPY .  /app/SYP-GradPot/

# WORKDIR /app/src/application/ssh
EXPOSE 2222

CMD ["python3", "hp_main.py"]
