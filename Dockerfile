# Use the official Python image as the base image
FROM python:3.11

# Install system dependencies for eSpeak-ng
RUN apt-get update && apt-get install -y \
    espeak-ng \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# Add debugging for system installation
RUN echo "Checking for eSpeak-ng installation..." && espeak-ng --version

# Set the working directory
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port your app runs on
EXPOSE 8080

# Run the app using gunicorn
CMD ["gunicorn", "-w", "4", "app:app"]
