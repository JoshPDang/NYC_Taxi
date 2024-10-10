import os
import subprocess
import zipfile
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Use home directory to avoid permission issues
HOME_DIR = os.path.expanduser("~")
CHROME_DIR = os.path.join(HOME_DIR, "chrome")
CHROMEDRIVER_DIR = os.path.join(HOME_DIR, "bin")

def download_and_install(url, extract_to, filename):
    """Download and extract a zip file from the provided URL."""
    print(f"Downloading from {url}...")
    local_filename = os.path.join(extract_to, filename)
    response = requests.get(url)
    with open(local_filename, 'wb') as file:
        file.write(response.content)
    print(f"Extracting {local_filename} to {extract_to}...")
    with zipfile.ZipFile(local_filename, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    os.remove(local_filename)
    print(f"Installation completed for {filename}.")

def install_google_chrome():
    """Download and install Google Chrome."""
    chrome_url = "https://storage.googleapis.com/chrome-for-testing-public/129.0.6668.70/mac-arm64/chrome-mac-arm64.zip"
    if not os.path.exists(CHROME_DIR):
        os.makedirs(CHROME_DIR, exist_ok=True)
    download_and_install(chrome_url, CHROME_DIR, "chrome-mac-arm64.zip")
    os.symlink(os.path.join(CHROME_DIR, "chrome-mac-arm64", "chrome"), os.path.join(HOME_DIR, "bin", "google-chrome"))
    print("Google Chrome installed successfully.")

def install_chromedriver():
    """Download and install ChromeDriver."""
    chromedriver_url = "https://storage.googleapis.com/chrome-for-testing-public/129.0.6668.70/mac-arm64/chromedriver-mac-arm64.zip"
    if not os.path.exists(CHROMEDRIVER_DIR):
        os.makedirs(CHROMEDRIVER_DIR, exist_ok=True)
    download_and_install(chromedriver_url, CHROMEDRIVER_DIR, "chromedriver-mac-arm64.zip")
    os.chmod(os.path.join(CHROMEDRIVER_DIR, "chromedriver"), 0o755)
    print("ChromeDriver installed successfully.")

# Installing Google Chrome and ChromeDriver
print("Downloading and installing Google Chrome...")
install_google_chrome()

print("Downloading and installing ChromeDriver...")
install_chromedriver()

# Set specific year and month for July 2024
current_year = 2024
month_name = "July"

# Set up Chrome options for Docker or Headless
chrome_options = Options()
chrome_options.add_argument("--headless")  # Ensure Chrome runs in headless mode
chrome_options.add_argument("--no-sandbox")  # Bypass OS security model, necessary for Docker
chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
chrome_options.add_argument("--disable-gpu")  # Disable GPU when running headless
chrome_options.add_argument("--window-size=1920,1080")  # Optional: Set window size for screenshots
chrome_options.add_argument("--remote-debugging-port=9222")  # Optional: Enable remote debugging

# Initialize the WebDriver
service = Service(os.path.join(CHROMEDRIVER_DIR, "chromedriver"))
driver = webdriver.Chrome(service=service, options=chrome_options)

# Open the TLC trip record page
url = "https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page"
driver.get(url)

# Wait for the page to load completely
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "p")))

# Extract the page source
page_source = driver.page_source

# Use BeautifulSoup to parse the page content
soup = BeautifulSoup(page_source, 'html.parser')

# Find the section with the target year
year_section = soup.find('p', string=str(current_year))  # Dynamically find target year

yellow_taxi_link = None  # Default to None in case not found
if year_section:
    month_section = year_section.find_next('strong', string=month_name)
    if month_section:
        yellow_taxi_link = month_section.find_next('a', title="Yellow Taxi Trip Records")
        if yellow_taxi_link:
            href = yellow_taxi_link.get('href')
            print(f"Yellow Taxi Trip Data Link for {month_name} {current_year}: {href}")

# Close the browser after scraping
driver.quit()

def download_file(url, local_filename):
    """
    Function to download a file from a given URL and save it locally.
    :param url: URL to the file
    :param local_filename: local path where the file should be saved
    """
    with requests.get(url, stream=True) as r:
        r.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                f.write(chunk)
    return local_filename

# Example usage: Download the file if the yellow taxi link was found
if yellow_taxi_link:
    href = yellow_taxi_link.get('href')
    print(f"Downloading Yellow Taxi Trip Data for {month_name} {current_year}...")
    file_path = download_file(href, f"yellow_tripdata_{current_year}-{month_name}.parquet")
    print(f"File downloaded successfully: {file_path}")
