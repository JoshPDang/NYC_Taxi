import os
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

# Detect if running inside Docker
IS_DOCKER = os.path.exists('/.dockerenv')

# Paths for Chrome and Chromedriver based on environment. You may need to change your paths
CHROME_BINARY_PATH = "/usr/bin/chromium" if IS_DOCKER else "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
CHROMEDRIVER_PATH = "/usr/bin/chromedriver" if IS_DOCKER else "/opt/homebrew/bin/chromedriver"

# Set Chrome options
chrome_options = Options()
chrome_options.binary_location = CHROME_BINARY_PATH
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")

# Initialize WebDriver
try:
    print(f"Using Chromedriver from: {CHROMEDRIVER_PATH}")
    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    print("Chromedriver initialized successfully.")
except Exception as e:
    print(f"Error initializing Chromedriver: {e}")
    exit(1)

# Open the TLC trip record page
url = "https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page"
print(f"Opening URL: {url}")

try:
    driver.get(url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "p")))
    print("Page loaded successfully.")
except Exception as e:
    print(f"Error loading the page: {e}")
    driver.quit()
    exit(1)

# Parse the page with BeautifulSoup
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Set the year and month
current_year = 2024
month_name = "February"
download_links = []  # List to store download link details

try:
    year_section = soup.find('p', string=str(current_year))
    if year_section:
        month_section = year_section.find_next('strong', string=month_name)
        if month_section:
            yellow_taxi_link = month_section.find_next('a', title="Yellow Taxi Trip Records")
            if yellow_taxi_link:
                href = yellow_taxi_link.get('href')
                print(f"Yellow Taxi Trip Data Link for {month_name} {current_year}: {href}")

                # Split the URL into base and relative parts
                base_url = "/".join(href.split("/")[:3])
                relative_url = "/".join(href.split("/")[3:])
                sink_filename = f"yellow_tripdata_{current_year}_{month_name}.parquet"

                # Append the link details to the list
                download_links.append({
                    "sourceBaseURL": base_url,
                    "sourceRelativeURL": relative_url,
                    "sinkFileName": sink_filename,
                    "sinkDirectory": month_name
                })
except Exception as e:
    print(f"Error parsing page content: {e}")

driver.quit()

# Save the download links as a JSON file
output_file = "download_links.json"
with open(output_file, "w") as f:
    json.dump(download_links, f, indent=4)

print(f"Download links saved to {output_file}.")

# Upload the JSON file to Azure Blob Storage
def upload_to_blob_storage(file_path, container_name, blob_name, connection_string):
    try:
        # Create a BlobServiceClient
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)

        # Get the container client
        container_client = blob_service_client.get_container_client(container_name)

        # # Create the container if it does not exist
        # container_client.create_container()

        # Get the BlobClient
        blob_client = container_client.get_blob_client(blob_name)

        # Upload the file
        with open(file_path, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)

        print(f"File '{file_path}' uploaded to container '{container_name}' as blob '{blob_name}'.")
    except Exception as e:
        print(f"Error uploading file to Blob Storage: {e}")

# Define your Azure Blob Storage details
CONNECTION_STRING = "your connection string"  # Replace with your connection string
CONTAINER_NAME = "config"  # Replace with your container name
BLOB_NAME = "download_links.json"  

# Upload the JSON file
upload_to_blob_storage(output_file, CONTAINER_NAME, BLOB_NAME, CONNECTION_STRING)
