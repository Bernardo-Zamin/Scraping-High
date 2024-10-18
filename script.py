from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import os
import re
import time

def sanitize_title(title):
    # Replace spaces, slashes, and other special characters with underscores
    return re.sub(r"[\\/\s]+", "_", title)

# Initialize the Chrome driver
driver = webdriver.Chrome()

url = 'https://highcompanybr.com/'
driver.get(url)

# Wait for the page to fully load
time.sleep(1)

# Scroll to the bottom of the page to load all products
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)  # Adjust the wait time as needed
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# Locate the products on the page
products = driver.find_elements(By.CSS_SELECTOR, '.products .product')

# Create a folder to save the images
os.makedirs('products', exist_ok=True)

# Iterate over the products and collect information
for product in products:
    try:
        image = product.find_element(By.TAG_NAME, 'img')
        title = product.find_element(By.CLASS_NAME, 'woocommerce-loop-product__title').text

        try:
            # Wait until the price is present or raise an exception if unavailable
            price = WebDriverWait(product, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'woocommerce-Price-amount'))
            ).text
            # Remove the space between 'R$' and the value
            price = price.replace('R$ ', 'R$')
        except:
            price = "SOLD-OUT"  # Set value to SOLD-OUT if the price is not found

        image_url = image.get_attribute('src')

        # Create a safe filename
        filename = f"{price}_{sanitize_title(title)}.jpg"
        full_path = os.path.join('products', filename)

        # Download the image
        if image_url:
            response = requests.get(image_url)
            with open(full_path, 'wb') as file:
                file.write(response.content)
    except Exception as e:
        print(f"Error processing product: {e}")

print("Scraping done!")

# Close the driver
driver.quit()
