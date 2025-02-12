# Use the official Python image as the base image
FROM python:3.11

# Install eSpeak-ng system dependency (text-to-speech library for pyttsx3)
RUN apt-get update && apt-get install -y \
    espeak-ng \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the project files into the container
COPY . .

# Install the required Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port your app runs on
EXPOSE 8080

# Run the app using Gunicorn
CMD ["gunicorn", "-w", "4", "app:app"]
