# Use the official Python image as the base image
FROM python:3.11

# Install system dependencies and other essential tools
RUN apt-get update && apt-get install -y \
    build-essential \
    espeak-ng \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install eSpeak-ng from the source
RUN git clone https://github.com/espeak-ng/espeak-ng.git /opt/espeak-ng && \
    cd /opt/espeak-ng && \
    make && \
    make install

# Check if eSpeak-ng is installed correctly
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
