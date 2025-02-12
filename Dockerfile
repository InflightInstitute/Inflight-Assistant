# Use the official Python image as the base image
FROM python:3.11

# Install system dependencies for eSpeak-ng
RUN apt-get update && apt-get install -y \
    espeak-ng \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app will run on
EXPOSE 8080

# Add a startup script to ensure eSpeak-ng is initialized correctly
CMD ["sh", "start.sh"]
