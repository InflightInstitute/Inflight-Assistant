FROM python:3.11

# Install system-level dependencies (for espeak-ng)
RUN apt-get update && apt-get install -y \
    espeak-ng \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy your project files into the container
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the application with Gunicorn
CMD ["gunicorn", "-w", "4", "app:app"]
