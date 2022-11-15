from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
from datetime import datetime

# URL
url = "https://www.sii.cl/valores_y_fechas/uf/uf2022.htm"
# Request
uf_html = requests.get(url).text
uf_soup = BeautifulSoup(uf_html,"lxml")

#Obteniendo tabla
df = pd.DataFrame(columns=["Ene","Feb","Mar","Abr","May","Jun","Jul","Ago","Sep","Oct","Nov","Dic"])
tabla_uf_2022 = uf_soup.find('div',{'id':'mes_all'})
tabla_final = tabla_uf_2022.find("table",{'id':'table_export'})


# Recoleccionando data de valores uf
for row in tabla_final.tbody.find_all('tr'):
    # Encontrar cada dato en la columna
    columnas = row.find_all('td')
    # Si es distinto a valor nulo
    if(columnas !=[]):
        enero = columnas[0].text.strip()
        febrero = columnas[1].text.strip()
        marzo = columnas[2].text.strip()
        abril = columnas[3].text.strip()
        mayo = columnas[4].text.strip()
        junio = columnas[5].text.strip()
        julio = columnas[6].text.strip()
        agosto = columnas[7].text.strip()
        septiembre = columnas[8].text.strip()
        octubre = columnas[9].text.strip()
        noviembre = columnas[10].text.strip()
        diciembre = columnas[11].text.strip()
        # Hacemos append al dataframe
        df = df.append({
                        "Ene":enero,
                        "Feb":febrero,
                        "Mar":marzo,
                        "Abr":abril,
                        "May":mayo,
                        "Jun":junio,
                        "Jul":julio,
                        "Ago":agosto,
                        "Sep":septiembre,
                        "Oct":octubre,
                        "Nov":noviembre,
                        "Dic":diciembre
                        },
                        ignore_index=True
                        )
# Reseteamos index para obtener los numeros del dia
df = df.reset_index()
df = df.rename(columns={"index":"Dia"})
df["Dia"] = df["Dia"].astype(int) # Transformamos a numero entero
df["Dia"] = df["Dia"] + 1 # Sumamos para eliminar el 0 y dejar formato sii

# Unpivot / Melt
df = df.melt("Dia",
            value_vars=["Ene","Feb","Mar","Abr","May","Jun","Jul","Ago","Sep","Oct","Nov","Dic"],
            var_name = "Mes",
            value_name = "valor_uf")
# Asignamos el año de la tabla
df["Ano"] = 2022

# Funcion para obtener numero de mes (hay librerias, pero el locale no funcionaba en español)
def mes_a_int(x):
    if x == "Ene":
        return 1
    if x == "Feb":
        return 2
    if x == "Mar":
        return 3
    if x == "Abr":
        return 4
    if x == "May":
        return 5
    if x == "Jun":
        return 6
    if x == "Jul":
        return 7
    if x == "Ago":
        return 8
    if x == "Sep":
        return 9
    if x == "Oct":
        return 10
    if x == "Nov":
        return 11
    if x == "Dic":
        return 12

# Creamos columna numero de mes
df["#Mes"] = df["Mes"].apply(mes_a_int)
# Creamos fecha final
df["Fecha"] = df["Dia"].astype(str)+"-"+df["#Mes"].astype(str)+"-"+df["Ano"].astype(str)
# Sacamos días que no existen!
df = df[~((df["Mes"]=="Feb")&(df["Dia"].isin([29,30,31])))]
# Cambiamos valores vacioes por NA
df = df.replace("",np.nan)
# Dropeamos valores vacios
df.dropna(inplace=True)
# Convertimos fecha a tipodato fecha
#df["Fecha"] = pd.to_datetime(df["Fecha"])
# Dropeamos mes porque ya no nos sirve
df.drop(columns="Mes", inplace=True)
# Reordenamos las columnas
df = df[["Fecha","Dia","#Mes","Ano","valor_uf"]]
df.drop(columns=["#Mes","Dia","Ano"],inplace=True)
# Creamos el archivo
df.to_csv("data.csv")






