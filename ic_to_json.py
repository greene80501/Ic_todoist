from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import time
import json

# Set up Selenium WebDriver
service = Service("C:/Users/green/Folders/.cache/selenium/chromedriver/win64/128.0.6613.137/chromedriver.exe")
driver = webdriver.Chrome(service=service)

try:
    # Navigate to the login page
    driver.get('https://login.microsoftonline.com/3e79b118-85d4-4b65-aae5-e76db24304b8/saml2?SAMLRequest=fZFbTwIxEIX%2FStP3vZW9lIaFEI0JiagR9MEXU7oDNtmdYqe78ee7IiT44uPccs75Zrb46lo2gCfrsOZZnHIGaFxj8VDzl%2B1dJPliPiPdteKoln34wGf47IECGw%2BR1O%2Bk5r1H5TRZUqg7IBWM2izX90rEqTp6F5xxLWe346FFHU5iHyEcSSVJ6w4W484a78jtg8PWIsTGdckEqukuy2QkiyaP8l1ZRFpDEUFVNjuRT9J8J5OTA85WtzV%2FL6daFkZKqKSsshx0VWSVLosC5H7SmGpcoydNZAeo%2BV63BD8d6mGFFDSGmotU5FE6jcR0K4TKK5WVcSGyN86evBtsA%2F5hzFfzFe4t2gDsRnfHnthm88jWGvUBPGevF55jen6mp046%2Fhrb%2F9RGm%2BB%2FSPH5hZQ1MQ0DNbHzh8SchBMKg9cWZ8m1yvxc%2Fn3Z%2FBs%3D&RelayState=%2Fstvrain%2Fportal%2Fstudents&sso_reload=true')

    # Enter email and click Next
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, 'i0116'))).send_keys('greene.wyatt30@svvsd.org')
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, 'idSIButton9'))).click()

    # Wait for the password field to appear and enter password
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.NAME, 'passwd')))
    driver.find_element(By.NAME, 'passwd').send_keys('2022Sv227199')

    # Click the "Sign In" button
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, 'idSIButton9'))).click()

    # Wait for any additional prompts and sign in automatically
    time.sleep(3)

    # If there's a "Stay signed in" prompt, click "Yes"
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'idSIButton9'))).click()
    except:
        pass

    # Wait for the login to complete
    WebDriverWait(driver, 20).until(EC.url_contains("https://ic.svvsd.org"))

    # Extract cookies from the Selenium session
    cookies = driver.get_cookies()

finally:
    driver.quit()

# Use the extracted cookies in a requests session
session = requests.Session()

# Add Selenium cookies to the requests session
for cookie in cookies:
    session.cookies.set(cookie['name'], cookie['value'])

# URL where the JSON data is available
json_url = 'https://ic.svvsd.org/campus/api/portal/assignment/listView'

# Send a GET request to the URL using the session with cookies
response = session.get(json_url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON data
    json_data = response.json()

    # Pretty print the JSON data to a file
    with open("assignments.json", "w") as w:
        w.write(json.dumps(json_data, indent=4))
else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")
