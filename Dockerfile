# Use the official Python image as the base image
FROM python:3.11

# Install dependencies and ensure that espeak-ng is installed properly
RUN apt-get update && apt-get install -y \
    espeak-ng \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Set the working directory
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app will run on
EXPOSE 8080

# Run the app using Gunicorn
CMD ["gunicorn", "-w", "4", "app:app"]
