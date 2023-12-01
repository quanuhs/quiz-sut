# Use an official Python runtime as a parent image
FROM --platform=linux/amd64 python:3.11.6-alpine3.18

# Set environment variables for Python (unbuffered mode) and Django
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create and set the working directory in the container
RUN mkdir -p /app
WORKDIR /app

# Copy the requirements file into the container and install dependencies
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Copy the rest of your Django project into the container
COPY . /app/

# Expose a port that your application will run on (e.g., 8000)
EXPOSE 8000

# Run Django's development server
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
