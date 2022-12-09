# Librerias
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options # Para configurar
from selenium.webdriver.support.ui import Select # Para seleccionar de listas desplegables
from selenium.webdriver.common.by import By # Para find_element
from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
import pandas as pd
import time
from datetime import datetime

# Webdriver
path = "C:/Users/chuck/Downloads/chromedriver_win32/chromedriver.exe"
# Configuraciones previas al webdriver para pagina Lider (es full Javascript)
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--nogpu")
chrome_options.add_argument("--disable-gpu")
#chrome_options.add_argument("--window-size=1280,1280")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--enable-javascript")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
# User agent
ua = UserAgent()
userAgent = ua.random 

# Obteniendo HTML
## Pan Jumbo (Desde el 1-12-2022 ahora la pag es generada por un js)
pan_jumbo_html = "https://www.jumbo.cl/marraqueta-grande-jumbo-v2-kg/p"
driver = Chrome(path, options=chrome_options)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
#driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": userAgent})
driver.get(pan_jumbo_html)
time.sleep(5)
pan_jumbo_soup = BeautifulSoup(driver.page_source, "html.parser")

### Obteniendo su precio
pan_jumbo = pan_jumbo_soup.find("span",class_="product-sigle-price-wrapper")
if pan_jumbo is None:
    while pan_jumbo is None:
        print("Intentando obtener el precio del Jumbo en 5 segundos...")
        time.sleep(5)
        pan_jumbo_soup = BeautifulSoup(driver.page_source, "html.parser")
        pan_jumbo = pan_jumbo_soup.find("span",class_="product-sigle-price-wrapper")
else:
    pan_jumbo = pan_jumbo_soup.find("span",class_="product-sigle-price-wrapper")
    print("Pude obtener el precio del pan del Jumbo!")

## Pan Lider
pan_lider_html = "https://www.lider.cl/supermercado/product/sku/333213/pan-pan-marraqueta-granel-500-g-5-un-aprox"
driver = Chrome(path, options=chrome_options)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": userAgent})
time.sleep(5)
driver.get(pan_lider_html)
pan_lider_soup = BeautifulSoup(driver.page_source,"html.parser")

### Obteniendo su precio

pan_lider = pan_lider_soup.find('span', class_='pdp-mobile-sales-price')
if pan_lider is None:
    while pan_lider is None:
        print("Intentando obtener precio del Lider en 5 segundos...")
        time.sleep(5)
        pan_lider_soup = BeautifulSoup(driver.page_source,"html.parser")
        pan_lider = pan_lider_soup.find('span', class_='pdp-mobile-sales-price')
else:
    pan_lider = pan_lider_soup.find('span', class_='pdp-mobile-sales-price')
    print("Pude obtener el precio del pan del Lider!")

## Pan Unimarc
pan_unimarc_html = requests.get("https://www.unimarc.cl/product/marraqueta-kg").text
pan_unimarc_soup = BeautifulSoup(pan_unimarc_html, "lxml")
### Obteniendo su precio
pan_unimarc = pan_unimarc_soup.find("div",class_="Text_text__cB7NM Text_text--left__1v2Xw Text_text--flex__F7yuI Text_text--semibold__MukSj Text_text--3xl__tLA7o Text_text--guardsman-red__wr1D8 Text_text__cursor--auto__cMaN1 Text_text--none__zez2n") # Que onda unimarc con los class?


# Print para chequear si tomo datos decentes
print(f"Precio 1/2 kilo marraqueta en el Jumbo {pan_jumbo.text}") # OK
print(f"Precio 1/2 kilo marraqueta en el Lider {pan_lider.text}") # OK
print(f"Precio 1/2 kilo marraqueta en el Unimarc {pan_unimarc.text}") # OK

### Lista

precios = []
supermercados = ["Jumbo","Lider","Unimarc"]
producto = ["Marraqueta 500g","Marraqueta 500g","Marraqueta 500g"]

### Agregamos los precios a la lista de precios

precios.append(pan_jumbo.text)
precios.append(pan_lider.text)
precios.append(pan_unimarc.text)

### Creamos diccionario
diccionario_pan = {
                "PRODUCTO": producto,
                "SUPERMERCADO":supermercados,
                "PRECIO":precios,
                "FECHA":"",
                "CATEGORIA":""
            }
### Transformarmos el diccionario a una dataframe
fecha_hoy = datetime.today().strftime('%Y-%m-%d') # La fecha de hoy formato "YY-mm-dd"
tabla_final = pd.DataFrame(diccionario_pan)
tabla_final["FECHA"] = fecha_hoy
tabla_final["CATEGORIA"] = "Pan"
tabla_final["PRECIO"] = tabla_final["PRECIO"].str.replace("$","",regex=True)
tabla_final["PRECIO"] = tabla_final["PRECIO"].str.replace(".","",regex=True)
tabla_final["PRECIO"] = tabla_final["PRECIO"].str.strip()

### Agregando la info a un dataset ya existente
tabla_final.to_csv("C:/Users/chuck/Documents/Clases y cursos/Python/Codeacademy/Webscraping/Proyecto/data-pan.csv",mode="a",index=False,header=False) # Ojo, es mejor asignat la ruta completa!, funciona sin ruta si estamos trabajando en una carepta de proyecto.