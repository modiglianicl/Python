# Web scraper servicentros (app_full.py)

Webscraping realizado con BS4 y Selenium para obtener direccion y precios de cada bencinera en Chile que venda Gasolina 97.
Usado para proyecto final en el diplomado en Inteligencia de Negocios PUC

# Chromedriver para selenium usado (Windows)

https://drive.google.com/file/d/18cGjvHNmvibR_fC2BDIvmHgeJJZcC6VZ/view?usp=sharing

Recomiendo dejarlo en : "C:/chromedriver_win32/"

Para MAC, googlear (jaja)

# Geopy y Google Geocoding API (analisis_df.ipynb)

También subí un notebook jupyter usando la API de Google Geocoding para obtener las coordenadas usando las direcciones, para luego agregarlo al dataset scrapeado.
Las direcciones que tiren error dejará las coordenadas (0,0) , estas deberán ser buscadas manualmente, recomiendo google maps. NECESITARAS TU API KEY la cual la puedes obtener de https://code.google.com/apis/console
