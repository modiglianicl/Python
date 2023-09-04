# Librerias
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
import pandas as pd
import requests
from bs4 import BeautifulSoup
from lxml import etree
import time


# Parametros y opciones del webdriver
service = Service(executable_path="C:/chromedriver_win32/chromedriver.exe")
opts = webdriver.ChromeOptions()
opts.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64)" + "AppleWebKit/537.36 (KHTML, like Gecko)" + "Chrome/51.0.2704.103 Safari/537.36")
opts.add_argument("--enable-javascript")
opts.add_experimental_option("excludeSwitches", ["enable-automation"])
opts.add_experimental_option("detach",True)

# I . Obteniendo regiones para iterar Regiones
## I . a Preparamos beautiful soup y pagina para scrapear
driver = webdriver.Chrome()
driver.get('http://www.bencinaenlinea.cl/web2/buscador.php?region=7')
time.sleep(5)
item_scrap_soup = BeautifulSoup(driver.page_source,"lxml")
## II. b Listado de todas las estaciones disponibles (para futuro regex)
regiones = []
regiones_raw = item_scrap_soup.find("select",id="reporte_region").find_all('option')
for i in regiones_raw:
    regiones.append(i.text)
print(f'Regiones detectadas : {regiones}')

# II. Preparamos DataFrame a llenar junto al archivo
df = pd.DataFrame(columns=["servicentro","direccion","region","autoservicio","precio","ultima_modificacion"])
df.to_csv("./db_estaciones.csv",index=False,header=True)


# III. Iteramos cada region detectada
for region in regiones:
    # Region
    region_actual = str(region)
    # Seteamos dirección del driver y argumentos de las opciones
    driver = webdriver.Chrome()
    # Le damos la url
    driver.get('http://www.bencinaenlinea.cl/web2/buscador.php?region=7')
    time.sleep(5)

    # Interacciones
    ## 1. Seleccionando región
    driver.find_element(By.ID,"reporte_region").click()
    region = Select(driver.find_element(By.ID,"reporte_region"))
    region.select_by_visible_text(region_actual)

    ## 2. Seleccionando Combustible
    driver.find_element(By.ID,"reporte_combustible").click()
    region = Select(driver.find_element(By.ID,"reporte_combustible"))
    region.select_by_visible_text('Gasolina 97')

    ## 3. Seleccionando todos los checkbox posibles
    comunas = driver.find_elements(By.NAME,"comuna")
    for comuna in comunas:
        comuna.click()

    ## 4. Generamos reporte con tabla
    driver.find_element(By.XPATH,"/html/body/table/tbody/tr[4]/td/table[1]/tbody/tr/td/table[1]/tbody/tr[6]/td/input").click() # Ya que es un "boton" dentro de una tabla sin id,sin class,solo me sirvió XPATH.

    time.sleep(5)



    ## 5.b. Preparamos beautiful soup
    item_scrap_soup = BeautifulSoup(driver.page_source,"lxml")
    ## 5.b.1 Listado de todas las estaciones disponibles (para futuro regex)
    estaciones_raw = item_scrap_soup.find("select",id="reporte_bandera").find_all('option')
    estaciones = []
    for i in estaciones_raw:
        estacion = i.text
        estaciones.append(estacion)

    ## 6. Identificamos tabla y filas
    ## 6.a Identificando tabla
    scrap_tabla = item_scrap_soup.find('div',id='tabla')
    tabla_final = scrap_tabla.find('table')

    ## 6.b Identificando filas
    ### Fila inicial (no la necesitamos)
    fila = 0

    # Iteramos en cada fila de la tabla
    for row in tabla_final.tbody.find_all('tr'):
        if fila == 0:
            fila = fila + 1
        else:
            # Obtenemos columnas
            columnas = row.find_all('td')
            print(f'Columnas detectadas : {columnas}')
            # Obtenemos nombre del servicentro
            servicentro_raw = columnas[0].text
            servicentro_split = servicentro_raw.split()
            servicentro_final = servicentro_split[0]
            for nombre in estaciones:
                if nombre in servicentro_final:
                    servicentro_final = nombre
            # Obtenemos direccion
            direccion = columnas[0].text
            for nombre in estaciones:
                if nombre in direccion:
                    direccion = direccion.replace(nombre,'')

            # Demas columnas
            autoservicio = columnas[1].text
            precio = columnas[2].text
            ultima_mod = columnas[3].text
            print(f'fila:{fila},servicentro : {servicentro_final}, dirección : {direccion},autoservicio?: {autoservicio}, precio: {precio}, last_update : {ultima_mod}')
            fila = fila +1

            # Append al DF

            df = df._append({
                            "servicentro": servicentro_final,
                            "direccion":  direccion,
                            "region" : region_actual,
                            "autoservicio": autoservicio,
                            "precio": precio,
                            "ultima_modificacion" : ultima_mod 
                            },ignore_index=True
                            )
    # Escribimos al archivo   
    df.to_csv("./db_estaciones.csv",index=False,header=False,mode="a")
    # Limpamos el dataframe!
    df = df[0:0]
    time.sleep(5)