# FROM python:3.9

# # Install necessary dependencies and Chrome
# RUN apt-get update -qq -y && \
#     apt-get install -y \
#         libasound2 \
#         libatk-bridge2.0-0 \
#         libgtk-4-1 \
#         libnss3 \
#         xdg-utils \
#         wget \
#         unzip \
#         libdrm2 \
#         libxkbcommon0 \
#         libxcomposite1 \
#         libxdamage1 \
#         libxrandr2 && \
#     wget -q -O chrome-linux64.zip https://bit.ly/chrome-linux64-121-0-6167-85 && \
#     unzip chrome-linux64.zip && \
#     rm chrome-linux64.zip && \
#     mv chrome-linux64 /opt/chrome/ && \
#     ln -s /opt/chrome/chrome /usr/local/bin/ && \
#     wget -q -O chromedriver-linux64.zip https://bit.ly/chromedriver-linux64-121-0-6167-85 && \
#     unzip -j chromedriver-linux64.zip chromedriver-linux64/chromedriver && \
#     rm chromedriver-linux64.zip && \
#     mv chromedriver /usr/local/bin/

# # Print Google Chrome version
# RUN google-chrome --version

# # Print ChromeDriver version
# RUN chromedriver --version

# # Clean up apt caches to reduce image size
# RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# # Set up working directory
# WORKDIR /app

# # Copy and install Python dependencies
# COPY requirements.txt .
# RUN pip install -r requirements.txt

# # Copy the scrape job file
# COPY scrape_job.py .

# # Run the scrape job script
# CMD ["python", "scrape_job.py"]


FROM python:3.9

# Install necessary system dependencies and Chrome
RUN apt-get update -qq -y && \
    apt-get install -y \
        wget \
        unzip \
        libasound2 \
        libatk-bridge2.0-0 \
        libgtk-4-1 \
        libnss3 \
        xdg-utils \
        libx11-xcb1 \
        libxcomposite1 \
        libxdamage1 \
        libxrandr2

# Download and install Google Chrome
RUN wget -q -O chrome-linux64.zip https://storage.googleapis.com/chrome-for-testing-public/129.0.6668.70/linux64/chrome-linux64.zip && \
    unzip chrome-linux64.zip -d /opt/chrome/ && \
    ln -s /opt/chrome/chrome-linux64/chrome /usr/local/bin/google-chrome && \
    rm chrome-linux64.zip

# Clean up apt caches to reduce image size
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Set up working directory
WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the scrape job file
COPY scrape_job.py .

# Run the scrape job script
CMD ["python", "scrape_job.py"]
