# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install netcat
RUN apt-get update && apt-get install -y netcat-openbsd

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt

# Copy the wait-for-it script
COPY wait-for-it.sh /usr/local/bin/wait-for-it.sh

# Run wait-for-it.sh to wait for the Kafka broker and then start the producer
CMD ["wait-for-it.sh", "broker", "9092", "--", "python", "transaction_producer.py"]