FROM python:3

WORKDIR /app/SYP-GradPot

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install Python dependencies
RUN pip3 install --upgrade pip
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt

# Copy the application code
COPY . /app/SYP-GradPot/

# Expose SSH port
EXPOSE 2222

CMD ["python3", "hp_main.py"]
