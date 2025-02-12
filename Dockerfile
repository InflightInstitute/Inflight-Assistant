# Use the official Python image as the base image
FROM python:3.11

# Install system-level dependencies for espeak-ng and other required libraries
RUN apt-get update && apt-get install -y \
    espeak-ng \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy your project files into the container
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port your app runs on
EXPOSE 8080

# Run the app with gunicorn
CMD ["gunicorn", "-w", "4", "app:app"]
