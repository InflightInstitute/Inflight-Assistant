#!/bin/bash

# Install system dependencies (eSpeak-ng)
echo "Installing eSpeak-ng..."
apt-get update
apt-get install -y espeak-ng

# Start the application
echo "Starting the app..."
exec gunicorn -w 4 app:app
