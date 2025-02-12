# Use the official Python image as the base image
FROM python:3.11

# Install system dependencies and eSpeak-ng from source
RUN apt-get update && apt-get install -y \
    build-essential \
    espeak-ng \
    libsndfile1 \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Check if espeak-ng is installed correctly
RUN echo "Checking if eSpeak-ng is installed..." && which espeak-ng && espeak-ng --version

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app will run on
EXPOSE 8080

# Run the app using gunicorn
CMD ["gunicorn", "-w", "4", "app:app"]
