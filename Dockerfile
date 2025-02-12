# Use the official Python image as the base image
FROM python:3.11

# Install system dependencies (for espeak-ng)
RUN apt-get update && apt-get install -y \
    espeak-ng \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /usr/src/app

# Copy the current directory into the container
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port your app runs on
EXPOSE 8080

# Run the app using Gunicorn
CMD ["gunicorn", "-w", "4", "app:app"]
