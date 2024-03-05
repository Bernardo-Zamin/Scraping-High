from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import os
import time

driver = webdriver.Chrome()

url = 'https://highcompanybr.com/'

driver.get(url)

time.sleep(1) 

last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1) 
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

produtos = driver.find_elements(By.CSS_SELECTOR, '.products .product')

if not os.path.exists('produtos'):
    os.makedirs('produtos')

for produto in produtos:
    imagem = produto.find_element(By.TAG_NAME, 'img')
    titulo = produto.find_element(By.CLASS_NAME, 'woocommerce-loop-product__title').text
    url_imagem = imagem.get_attribute('src')

    nome_arquivo = titulo.replace(" ", "_").replace("/", "_").replace("\\", "_") + '.jpg'
    caminho_completo = os.path.join('produtos', nome_arquivo)

    print(url_imagem, "->", caminho_completo)

    if url_imagem:
        response = requests.get(url_imagem)
        with open(caminho_completo, 'wb') as file:
            file.write(response.content)


driver.quit()
