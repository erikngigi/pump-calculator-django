# Use an offical python runtime as a parent image
FROM python:3.12

# Set environmental variables
ENV PYTHONDONTWRITEBYCODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Copt the project code into the container
COPY . /app/
