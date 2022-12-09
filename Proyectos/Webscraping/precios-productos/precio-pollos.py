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
#chrome_options.add_argument("--window-size=1280,1280") # Desactivado, me traia problemas con algunas páginas!
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--enable-javascript")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
# User agent driver
#ua = UserAgent()
#userAgent = ua.random
# Cargando datasets... en caso de ser requerido
data_pollos = pd.read_csv('data-pollos.csv')
# Funcion scraper selenium
def selenium_scrap(url,supermercado,elemento,clase,nombre_producto):
    driver = Chrome(path, options=chrome_options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    #driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": userAgent})
    driver.get(url)
    print(f"Esperando 5 segundos para que cargue bien la página...")
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source,"lxml")
    precio = soup.find(elemento,class_=clase)
    if precio is None:
        while precio is None:
            print(f"Intentando obtener precio de {nombre_producto} desde {supermercado} en 5 segundos...")
            time.sleep(5)
            soup = BeautifulSoup(driver.page_source,"lxml")
            precio = soup.find(elemento,class_=clase)
    else:
        precio = soup.find(elemento,class_=clase)
        print(f"Pude obtener el precio de {nombre_producto} desde {supermercado}!")
    return precio


# Obteniendo HTML

# Pechuga deshuesada 700 g
## Ariztia
### Lider (Necesito Selenium)
pollo_lider_ariztia_700g = "https://www.lider.cl/supermercado/product/sku/344025/super-pollo-pollo-pechuga-deshuesada-congelada-700-g"
driver = Chrome(path, options=chrome_options)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
#driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": userAgent})
driver.get(pollo_lider_ariztia_700g)
time.sleep(5)
pollo_lider_ariztia_700g_soup = BeautifulSoup(driver.page_source,"lxml")
precio_lider_ariztia_700g = pollo_lider_ariztia_700g_soup.find("span",class_="pdp-mobile-sales-price")
#### Si el elemento que trae es vacío...
if precio_lider_ariztia_700g is None:
    while precio_lider_ariztia_700g is None:
        print("Intentando obtener precio del Lider en 5 segundos...")
        time.sleep(5)
        pollo_lider_ariztia_700g_soup = BeautifulSoup(driver.page_source,"html.parser")
        precio_lider_ariztia_700g = pollo_lider_ariztia_700g_soup.find('span', class_='pdp-mobile-sales-price')
else:
    precio_lider_ariztia_700g = pollo_lider_ariztia_700g_soup.find('span', class_='pdp-mobile-sales-price')
    print("Pude obtener el precio del pollo Ariztia 700g del Lider!")

### Unimarc
pollo_unimarc_ariztia_700g = requests.get("https://www.unimarc.cl/product/pechuga-deshuesada-de-pollo-ariztia-700-g").text #OK
pollo_unimarc_ariztia_700g_soup = BeautifulSoup(pollo_unimarc_ariztia_700g,"lxml")
precio_unimarc_ariztia_700g = pollo_unimarc_ariztia_700g_soup.find("div",class_="Text_text__cB7NM Text_text--left__1v2Xw Text_text--flex__F7yuI Text_text--semibold__MukSj Text_text--3xl__tLA7o Text_text--guardsman-red__wr1D8 Text_text__cursor--auto__cMaN1 Text_text--none__zez2n")
if precio_unimarc_ariztia_700g is None:
    precio_unimarc_ariztia_700g = str(int(data_pollos[(data_pollos['MARCA'] == 'Ariztia') & (data_pollos['SUPERMERCADO'] == 'Unimarc')].groupby('PRODUCTO')['PRECIO'].mean()[0]))
else:
    precio_unimarc_ariztia_700g = pollo_unimarc_ariztia_700g_soup.find("div",class_="Text_text__cB7NM Text_text--left__1v2Xw Text_text--flex__F7yuI Text_text--semibold__MukSj Text_text--3xl__tLA7o Text_text--guardsman-red__wr1D8 Text_text__cursor--auto__cMaN1 Text_text--none__zez2n").text

### Tottus (Necesito Selenium)
pollo_tottus_ariztia_700g = "https://tottus.falabella.com/tottus-cl/product/110622839/ariztia-pechuga-de-pollo-deshuesada-marinada-20345777/110622842?exp=tottus"
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
#driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": userAgent})
driver.get(pollo_tottus_ariztia_700g)
time.sleep(5)
pollo_tottus_ariztia_700g_soup = BeautifulSoup(driver.page_source,"lxml")
precio_tottus_ariztia_700g = pollo_tottus_ariztia_700g_soup.find("div",class_="jsx-2797633547 cmr-icon-container")
#### Si el elemento que trae es vacío...
if precio_tottus_ariztia_700g is None:
    while precio_tottus_ariztia_700g is None:
        print("Intentando obtener precio del Tottus en 5 segundos...")
        time.sleep(5)
        pollo_tottus_ariztia_700g_soup = BeautifulSoup(driver.page_source,"html.parser")
        precio_tottus_ariztia_700g = pollo_tottus_ariztia_700g_soup.find("div",class_="jsx-2797633547 cmr-icon-container")
else:
    precio_tottus_ariztia_700g = pollo_tottus_ariztia_700g_soup.find("div",class_="jsx-2797633547 cmr-icon-container")
    print("Pude obtener el precio del pollo Ariztia 700g del Tottus!")

### Jumbo
pollo_jumbo_ariztia_700g = "https://www.jumbo.cl/pechuga-deshuesada-de-pollo-ariztia-700-g/p"
driver = Chrome(path, options=chrome_options)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
#driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": userAgent})
driver.get(pollo_jumbo_ariztia_700g)
time.sleep(5)
pollo_jumbo_ariztia_700g_soup = BeautifulSoup(driver.page_source,"html.parser")
precio_jumbo_ariztia_700g = pollo_jumbo_ariztia_700g_soup.find("span",class_="price-best")

if precio_jumbo_ariztia_700g is None:
    while precio_jumbo_ariztia_700g is None:
        print("Intentando obtener precio del Jumbo en 5 segundos...")
        time.sleep(5)
        driver.get(pollo_jumbo_ariztia_700g)
        pollo_jumbo_ariztia_700g_soup = BeautifulSoup(driver.page_source,"html.parser")
        precio_jumbo_ariztia_700g = pollo_jumbo_ariztia_700g_soup.find("span",class_="price-best")
else:
    precio_jumbo_ariztia_700g = pollo_jumbo_ariztia_700g_soup.find("span",class_="price-best")
    print("Pude obtener el precio del pollo Ariztia 700g del Jumbo!")

## Super Pollo
### Lider (Necesito Selenium)
pollo_lider_superpollo_700g = "https://www.lider.cl/supermercado/product/sku/344025/super-pollo-pollo-pechuga-deshuesada-congelada-700-g"
driver = Chrome(path, options=chrome_options)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
#driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": userAgent})
driver.get(pollo_lider_superpollo_700g)
time.sleep(5)
pollo_lider_superpollo_700g_soup = BeautifulSoup(driver.page_source,"html.parser")
precio_lider_superpollo_700g = pollo_lider_superpollo_700g_soup.find("span",class_="pdp-mobile-sales-price")
#### Si el elemento que trae es vacío...
if precio_lider_superpollo_700g is None:
    while precio_lider_superpollo_700g is None:
        print("Intentando obtener precio del Lider en 5 segundos...")
        time.sleep(2)
        driver.get(pollo_lider_superpollo_700g)
        pollo_lider_superpollo_700g_soup = BeautifulSoup(driver.page_source,"html.parser")
        precio_lider_superpollo_700g = pollo_lider_superpollo_700g_soup.find("span",class_="pdp-mobile-sales-price")
else:
    precio_lider_superpollo_700g = pollo_lider_superpollo_700g_soup.find("span",class_="pdp-mobile-sales-price")
    print("Pude obtener el precio del pollo Superpollo 700g del Lider!")
### Unimarc
pollo_unimarc_superpollo_700g = requests.get("https://www.unimarc.cl/product/pechuga-pollo-deshuesada-super-pollo-700-g").text #OK
pollo_unimarc_superpollo_700g_soup = BeautifulSoup(pollo_unimarc_superpollo_700g,"html.parser")
precio_unimarc_superpollo_700g = pollo_unimarc_superpollo_700g_soup.find("div",class_="Text_text__cB7NM Text_text--left__1v2Xw Text_text--flex__F7yuI Text_text--semibold__MukSj Text_text--3xl__tLA7o Text_text--guardsman-red__wr1D8 Text_text__cursor--auto__cMaN1 Text_text--none__zez2n")

### Tottus (Necesito Selenium)
pollo_tottus_superpollo_700g = "https://tottus.falabella.com/tottus-cl/product/110623283/super-pollo-pechuga-de-pollo-deshuesada-congelada-20155420/110623284?exp=tottus"
driver = Chrome(path, options=chrome_options)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
#driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": userAgent})
driver.get(pollo_tottus_superpollo_700g)
time.sleep(5)
pollo_tottus_superpollo_700g_soup = BeautifulSoup(driver.page_source,"html.parser")
precio_tottus_superpollo_700g = pollo_tottus_superpollo_700g_soup.find("span",class_="copy12 primary medium jsx-2889528833 normal      line-height-29")
#### Si el elemento que trae es vacío...
if precio_tottus_superpollo_700g is None:
    while precio_tottus_superpollo_700g is None:
        print("Intentando obtener precio del Tottus en 2 segundos...")
        time.sleep(2)
        pollo_tottus_superpollo_700g_soup = BeautifulSoup(driver.page_source,"html.parser")
        precio_tottus_superpollo_700g = pollo_tottus_superpollo_700g_soup.find("div",class_="jsx-2797633547 cmr-icon-container")
else:
    precio_tottus_superpollo_700g = pollo_tottus_superpollo_700g_soup.find("div",class_="jsx-2797633547 cmr-icon-container")
    print("Pude obtener el precio del pollo Superpollo de 700g del Tottus!")
### Jumbo
pollo_jumbo_superpollo_700g = "https://www.jumbo.cl/pechuga-deshuesada-de-pollo-super-pollo-700-g/p"
#pollo_jumbo_superpollo_700g_soup = BeautifulSoup(pollo_jumbo_superpollo_700g,"lxml")
precio_jumbo_superpollo_700g = selenium_scrap(pollo_jumbo_superpollo_700g,'Jumbo',"span","price-best","Pechuga deshuesada superpollo 700g")


# Probando precios Ariztia
print('Precios Pechuga deshuesada 700g ARIZTIA')
print(f'Precio Lider : {precio_lider_ariztia_700g.text}')
print(f'Precio Unimarc: {precio_unimarc_ariztia_700g}')
print(f'Precio Tottus : {precio_tottus_ariztia_700g.text}')
print(f'Precio Jumbo : {precio_jumbo_ariztia_700g.text}')

# Probando precios SuperPollo
print('\nPrecios Pechuga deshuesada 700g SuperPollo\n')
print(f'Precio Lider : {precio_lider_superpollo_700g.text}')
print(f'Precio Unimarc : {precio_unimarc_superpollo_700g.text}')
print(f'Precio Tottus : {precio_tottus_superpollo_700g.text}')
print(f'Precio Jumbo : {precio_jumbo_superpollo_700g.text}')

# Creando diccionario para Ariztia
## Listas Ariztia
precios_ariztia = []
precios_ariztia.append(precio_lider_ariztia_700g.text)
precios_ariztia.append(precio_unimarc_ariztia_700g)
precios_ariztia.append(precio_tottus_ariztia_700g.text)
precios_ariztia.append(precio_jumbo_ariztia_700g.text)
supermercados = ["Lider","Unimarc","Tottus","Jumbo"]
## Creacion diccionario

diccionario_ariztia = {
                "PRODUCTO" : "",
                "MARCA" : "",
                "SUPERMERCADO" : supermercados,
                "PRECIO" : precios_ariztia,
                "FECHA" : "",
                "CATEGORIA" : ""
                        }
## Pasando a DF
fecha_hoy = datetime.today().strftime('%Y-%m-%d') # La fecha de hoy formato "YY-mm-dd"
tabla_ariztia = pd.DataFrame(diccionario_ariztia)
tabla_ariztia["PRODUCTO"] = "Pechuga deshuesada 700g"
tabla_ariztia["MARCA"] = "Ariztia"
tabla_ariztia["FECHA"] = fecha_hoy
tabla_ariztia["CATEGORIA"] = "Pollo"

# Creando diccionario para Superpollo
## Listas SuperPollo
precios_superpollo = []
precios_superpollo.append(precio_lider_superpollo_700g.text)
precios_superpollo.append(precio_unimarc_superpollo_700g.text)
precios_superpollo.append(precio_tottus_superpollo_700g.text)
precios_superpollo.append(precio_jumbo_superpollo_700g.text)
diccionario_superpollo =  {
                "PRODUCTO" : "",
                "MARCA" : "",
                "SUPERMERCADO" : supermercados,
                "PRECIO" : precios_superpollo,
                "FECHA" : "",
                "CATEGORIA" : ""
                        }
## Pasando a DF

tabla_superpollo = pd.DataFrame(diccionario_superpollo)
tabla_superpollo["PRODUCTO"] = "Pechuga deshuesada 700g"
tabla_superpollo["MARCA"] = "Super Pollo"
tabla_superpollo["FECHA"] = fecha_hoy
tabla_superpollo["CATEGORIA"] = "Pollo"

# Tabla final
tabla_final = pd.concat([tabla_ariztia, tabla_superpollo])
tabla_final["PRECIO"] = tabla_final["PRECIO"].str.replace("$","",regex=True)
tabla_final["PRECIO"] = tabla_final["PRECIO"].str.replace(".","",regex=True)
tabla_final["PRECIO"] = tabla_final["PRECIO"].str.strip()
tabla_final.to_csv("C:/Users/chuck/Documents/Clases y cursos/Python/Codeacademy/Webscraping/Proyecto/data-pollos.csv",index=False,mode="a",header=False)