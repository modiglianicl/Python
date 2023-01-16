# Librerias
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.support.ui import Select 
from selenium.webdriver.common.by import By 
from bs4 import BeautifulSoup
import requests
import pandas as pd
import time

# Webdriver
path = "path al chromedriver.exe"
# Argumentos para el webdriver
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--nogpu")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--enable-javascript")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.add_argument('--disable-blink-features=AutomationControlled')

# Scrapeo con rango (el id de item en RO parte en 501)
for i in range(501,22000):
    # Creacion dataframe
    df = pd.DataFrame(columns=["Fecha","ID_ITEM","Merchant","Item","Precio","Carta","RandomOptions","Icono","Imagen"])
    item_id = str(i)
    item_scrap_url = "https://projectalfheim.net/?module=market&action=item&stype=1&itemid="+item_id+"&card_id=&refine=&enhants=&egrade=0"
    driver = Chrome(path, options=chrome_options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.get(item_scrap_url)
    time.sleep(5) # Necesario, ya que si no esperamos, no mostrara nada...
    item_scrap_soup = BeautifulSoup(driver.page_source,"lxml")
    scrap_tabla = item_scrap_soup.find('table',class_='horizontal-table')
    # Obteniendo icono item
    icono_item_raw = item_scrap_soup.find('img',class_='icon_image')['src']
    url_icono = "https://projectalfheim.net"+icono_item_raw
    # Obteniendo imagen item
    tabla_info = item_scrap_soup.find('table',class_='vertical-table')
    imagen_item_raw = tabla_info.tbody.find('img')['src']
    url_imagen = "https://projectalfheim.net"+imagen_item_raw

    # Scrapeo tabla precios
    for row in scrap_tabla.tbody.find_all('tr'):
        columnas = row.find_all('td')
        # Las columnas seran 7 cuando es un item que no es equipo
        if(columnas !=[] and len(columnas)==7):
            fecha = columnas[0].text.strip()
            merchant = columnas[1].text.strip()
            nombre_item = columnas[5].text.strip()
            precio = columnas[6].text.strip().replace('?','')
            carta = "NULL"
            random_options = "NULL"
            # Append al df
            df = df.append({
                            "Fecha":fecha,
                            "ID_ITEM":item_id,
                            "Merchant":merchant,
                            "Item":nombre_item,
                            "Precio":precio,
                            "Carta":carta,
                            "RandomOptions":random_options,
                            "Icono":url_icono,
                            "Imagen":url_imagen
                            },ignore_index=True
                        )
        # Cuando es equipo las columnas son 9 ya que incluye la carta y los random rolls
        if(columnas !=[] and len(columnas)==9):
            fecha = columnas[0].text.strip()
            merchant = columnas[1].text.strip()
            nombre_item = columnas[5].text.strip()
            precio = columnas[6].text.strip().replace('?','')
            carta = columnas[7].text.strip()
            random_options = columnas[8].text.replace('\n','').strip()
            # Append al df
            df = df.append({
                            "Fecha":fecha,
                            "Merchant":merchant,
                            "ID_ITEM":item_id,
                            "Item":nombre_item,
                            "Precio":precio,
                            "Carta":carta,
                            "RandomOptions":random_options,
                            "Icono":url_icono,
                            "Imagen":url_imagen
                            },ignore_index=True
                        )

    # Configuracion DataFrame
    print(f"Agregando el item ID {item_id}")
    df = df.reset_index()
    df = df.drop(columns="index")
    # Dejamos precio como valor entero
    df['Precio'] = df['Precio'].astype(int)
    # Reemplazamos las distintas ocurrencias de espacios que ocurren con un @ para separar cada roll de stats!
    df['RandomOptions'] = df['RandomOptions'].replace(to_replace='\s{14}',value='@',regex=True)
    df['Carta'] = df['Carta'].replace(to_replace='\s{13}',value='@',regex=True)
    df['Carta'] = df['Carta'].replace(to_replace='\n',value='',regex=True)
    print(df)
    # Antes de comenzar el script recomiendo crear un .csv con las columnas, ya que esta en modo append.
    df.to_csv("/Scrapper Afelheim/db_precios.csv",index=False,header=False,mode="a") 
    df = df[0:0] # Reseteamos el dataframe para el proximo item

