# Librerias
from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
from datetime import date

# Obteniendo HTML
buscar = "razer black widow chroma v2".replace(" ","%20")
filtro = None # Este filtro, eliminara cualquier producto que contenga esta palabra
html_text = requests.get('https://listado.mercadolibre.cl/razer-black-widow-chroma-v2#D[A:+buscar+,L:undefined]').text
# print(html_text) # Imprime...
# Parser
soup = BeautifulSoup(html_text,"lxml")

# Probemos con solo un item (con el primero del tag)
item = soup.find("li",class_="ui-search-layout__item shops__layout-item")
title_1 = item.find("h2",class_="ui-search-item__title shops__item-title").text
precio_1 = item.find("span",class_="price-tag-fraction").text
envio_gratis_1 = item.find("p",class_="ui-search-item__shipping ui-search-item__shipping--free shops__item-shipping-free").text

resultado_1 = print(f'''
Producto: {title_1}
Precio: ${precio_1}
{envio_gratis_1}
''')

# Ahora para todos
items = soup.find_all("li",class_="ui-search-layout__item shops__layout-item")


# Preparemos las listas que iran a un Dataframe

item_title = []
item_precio = []
item_link = []
item_enviog = []

# Iteramos
def search_item():
    for item in items:
        envio_gratis = item.find("p",class_="ui-search-item__shipping ui-search-item__shipping--free shops__item-shipping-free")
        if envio_gratis is None: # Su envio_gratis no logra obtener un valor...
                envio_gratis = "No"
                item_enviog.append(envio_gratis)
        elif "gratis" in envio_gratis.text: # Si está la palabra "gratis" en envio gratis que nos avise!
            envio_gratis = "Si"
            item_enviog.append(envio_gratis)
        title = item.find("h2",class_="ui-search-item__title shops__item-title").text
        item_title.append(title.replace(","," ")) # Mas que nada elimine comas, ya que daban problemas al convertir en Excel.
        if filtro is not None:
            if filtro not in title: # Si el filtro definido no esta que muestre...
                    precio = item.find("span",class_="price-tag-fraction").text
                    link = item.find("a",class_="ui-search-item__group__element shops__items-group-details ui-search-link").get("href")
                    item_precio.append(precio)
                    item_link.append(link)
        else:
            precio = item.find("span",class_="price-tag-fraction").text
            link = item.find("a",class_="ui-search-item__group__element shops__items-group-details ui-search-link").get("href")
            item_precio.append(precio)
            item_link.append(link)

        # Resultados
        print(f'Producto: {title}')
        print(f'Precio: ${precio}')
        print(f'Envio gratis: {envio_gratis}')
        print(f'Link: {link}')

        # Creamos el dataframe

        df = pd.DataFrame({
                    "PRODUCT_NAME":item_title,
                    "PRODUCT_PRICE":item_precio,
                    "FREE_DELIVERY":item_enviog,
                    "PRODUCT_LINK":item_link
        })
    return df
# Creando archivo CSV
fecha = date.today()
fecha_archivo = str(fecha).replace("-","")
df = search_item()
df.to_csv(buscar.replace("%20","-")+"-mercadolibre-"+fecha_archivo+".csv",index = None, header= True)

print(fecha_archivo)
# Hagamos esta lista cada 900 segundos
#if __name__ == '__main__':
#    while True:
#        search_item()
#        wait = 20 # Minutos
#        print(f"Esperando {wait} minutos...")
#        time.sleep(60 * wait)
