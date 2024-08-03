import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Set up Chrome options
chrome_options = Options()
# Add options as needed, e.g., chrome_options.add_argument("--headless")

# Specify the path to ChromeDriver
service = Service(executable_path=r'C:\Users\danie\Downloads\chromedriver-win64\chromedriver.exe')

# Initialize the driver with the specified service and options
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get('http://www.google.com/')
time.sleep(5)  # Let the user actually see something

# Use By.NAME for locating the search box element
search_box = driver.find_element(By.NAME, 'q')
search_box.send_keys('ChromeDriver')
search_box.submit()
time.sleep(20)  # Let the user actually see something

driver.quit()
