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

# Add an argument to specify the Python script
ARG script=normal_transaction_producer.py

# Set an environment variable for the script
ENV SCRIPT_NAME=${script}

# Ensure the wait-for-it script is executable
RUN chmod +x /usr/local/bin/wait-for-it.sh

# Running wait-for-it.sh script first to ensure broker is available and live before script start producing transactions.
CMD ["sh", "-c", "/usr/local/bin/wait-for-it.sh broker 9092 -- python /app/${SCRIPT_NAME}"]