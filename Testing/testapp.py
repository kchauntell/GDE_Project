from test_logs import logger
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import argparse


parser = argparse.ArgumentParser(description='Testing Code for Weather Application')
parser.add_argument('--zip', type=str, help='Zip code', required=True)
parser.add_argument('--location', type=str, help='City of given Zip code', required=True)
parser.add_argument('--app_address', type=str, help='URL address to WeatherApp', required=True)

args = parser.parse_args()
zip = args.zip
location = args.location
app_address = args.app_address

geckodriver_path = "/snap/bin/geckodriver"
service = Service(executable_path=geckodriver_path)

#Headless mode
options = Options()
options.add_argument("--headless") #browser window will not be displayed
options.add_argument("--disable-gpu") #disables gpu hardware acceleration

driver = webdriver.Firefox(service=service, options=options)

def wait_for_element(kind, name):
    if kind == "class":
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, name))
        )
    elif kind == "link_text":
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, name))
        )

def test(zip, location, app_address):
    logger.debug("Starting test, attempting to access {app_address}")
    try:
        driver.get(app_address) #"http://localhost:8080"
    except Exception as e :
        logger.error(f"Failed to access {app_address} due to {e}")
        return ("Test Failed: Accessing App Address")

    logger.debug(f"Waiting for input element")
    wait_for_element("id", "name")
    try:
        input_element = driver.find_element(By.ID, "name")
        input_element.send_keys(zip + Keys.RETURN)
    except Exception as e:
        logger.error(f"Failed to send keys to input element due to {e}")
        return ("Test Failed: Sending Keys to Input Element")
    
    logger.debug(f"Waiting for answer element")
    time.sleep(15)
    try:
        location_element = driver.find_element(By.ID, "Location")
        city = location_element.text.split('Location: ')[1].split(', ')[0]
    except Exception as e:
        logger.error(f"Failed to get location element due to {e}")
        return ("Test Failed: Obtaining location element")
    
    logger.debug(f"Closing browser.")
    try:
        driver.quit()
    except Exception as e:
        logger.error(f"Failed to close browser due to {e}")
        return ("Test Failed: Closing Browser")
    
    logger.debug(f"Comparing {city} with {location}")
    if city == location:
        return("Test Passed")
    else:
        return("Test Failed")
    


result = test(zip, location, app_address)
print(result)