from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import time

# Arreglo para almacenar los links
enlaces_guardados = []

# Configurar Selenium para usar Chrome
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Abrir la URL
driver.get('https://voyalteatro.com')
time.sleep(2)
select_element = driver.find_element("tag name", "select") 
select = Select(select_element)
select.select_by_value('14')  # 14 corresponde a Jalisco
time.sleep(2)

# Abrir la cartelera del dia
driver.get('https://voyalteatro.com/cartelera?date=2024-11-27')
time.sleep(2)
html = driver.page_source # Obtener el HTML una vez que el contenido ha sido cargado por JavaScript
soup = BeautifulSoup(html, 'html.parser')

# Buscar eventos
titulos = soup.find_all('p', class_='event-name')
if not titulos:
    print("No hay eventos disponibles")

else:
    for titulo in titulos:
        print(titulo.text)

    # Buscar enlaces
    enlaces = soup.find_all('a', href=True)
    for enlace in enlaces:
        if enlace['href'].startswith('/cartelera/'):
            enlaces_guardados.append(enlace['href'])

    for enlace in enlaces_guardados:
        driver.get('https://voyalteatro.com' + enlace)
        time.sleep(5)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        sinopsis = soup.find('p', class_='event-section-content')
        print('https://voyalteatro.com' + enlace)
        print(sinopsis.text)
        time.sleep(2)

driver.quit()