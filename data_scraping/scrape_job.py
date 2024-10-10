from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests
import time

# Set specific year and month for July 2024
current_year = 2024
month_name = "July"

# Set up Chrome options for Docker
chrome_options = Options()
chrome_options.add_argument("--headless")  # Ensures Chrome runs in headless mode
chrome_options.add_argument("--no-sandbox")  # Required for Docker
chrome_options.add_argument("--disable-dev-shm-usage")  # Overcomes limited resource problems
chrome_options.add_argument("--disable-gpu")  # Optional: applicable only if you have GPU problems

# Automatically download and manage ChromeDriver with webdriver-manager
service = Service(ChromeDriverManager().install())
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

# Example usage
if yellow_taxi_link:
    href = yellow_taxi_link.get('href')
    print(f"Downloading Yellow Taxi Trip Data for {month_name} {current_year}...")
    file_path = download_file(href, f"yellow_tripdata_{current_year}-{month_name}.parquet")
    print(f"File downloaded successfully: {file_path}")






