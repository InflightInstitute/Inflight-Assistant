#!/bin/bash

# Ensure system dependencies are installed
echo "Installing eSpeak-ng..."
apt-get update
apt-get install -y espeak-ng

# Start the application using Gunicorn
echo "Starting the application..."
exec gunicorn -w 4 app:app
