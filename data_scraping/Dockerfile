# Use the official Python slim image
FROM python:3.9-slim

ENV DEBIAN_FRONTEND=noninteractive

# Install necessary packages including Chromium and Chromedriver
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    libglib2.0-0 \
    libnss3 \
    libgconf-2-4 \
    libxss1 \
    fonts-liberation \
    libappindicator3-1 \
    libgbm1 \
    xdg-utils \
    dbus-x11 \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Set the PATH to include Chromium and Chromedriver
ENV PATH="/usr/bin:$PATH"

# Copy requirements and install Python dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the Python script into the container
COPY scrapejob.py /app/scrapejob.py

# Set the working directory
WORKDIR /app

# Set the default command to run the script
CMD ["python", "scrapejob.py"]
