# Use an official Debian-based image to have full control over system-level dependencies
FROM debian:bullseye-slim

# Install Python 3, pip, and system dependencies (eSpeak-ng)
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    espeak-ng \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# Install the required Python packages
RUN pip3 install --no-cache-dir -r requirements.txt

# Set the working directory
WORKDIR /usr/src/app

# Copy the current directory contents into the container
COPY . .

# Expose the port your app runs on
EXPOSE 8080

# Run the app using gunicorn
CMD ["gunicorn", "-w", "4", "app:app"]
