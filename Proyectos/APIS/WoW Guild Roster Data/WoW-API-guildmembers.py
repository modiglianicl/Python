# Librerias

import requests
import json
from requests.auth import HTTPBasicAuth
import pandas as pd
import time

# Funcion para obtener el access token

def create_access_token(client_id, client_secret):
    url = "https://oauth.battle.net/token"
    body = {"grant_type": 'client_credentials'}
    auth = HTTPBasicAuth(client_id, client_secret)

    response = requests.post(url, data=body, auth=auth)
    return response.json()

########### DATOS A CAMBIAR ###########

# Obteniendo access token 
access_token = create_access_token("Client ID ACA","Cliente SECRET ACA")['access_token'] # Primer argumento es clientid, segundo argumento client secret, esto lo puedes obtener desde la pagina de blizzard
# Datos guild y opciones
realm_guild = 'ragnaros' # Nombre del realm en minusculas
nombre_guild = 'silver-sword' # Nombre de la guild ,todo en minuscula, espacios deben ser "-" (guiones)
idioma_datos = "es_MX" # Localización, para el idioma de los datos a obtener, español latino = "es_MX" , ingles NA = "en_US" , mas info : https://develop.battle.net/documentation/world-of-warcraft/guides/localization

########### FIN DATOS A CAMBIAR ###########

# Endpoint y GET
headers = {"Authorization" : f"Bearer {access_token}"}
url_wow = f"https://us.api.blizzard.com/data/wow/guild/{realm_guild}/{nombre_guild}/roster?namespace=profile-us&locale={idioma_datos}"
response = requests.get(url_wow,headers=headers)
data = response.json()

# Cantidad de miembros
guild_len = len(data['members'])

# Listas para el DF
nombres = []
niveles = []
realms = []
facciones = []
razas = []
clases = []
specs_activas = []
item_lvls = []
rating_miticas = []
mejores_llaves = []
nombre_mejores_llaves = []
lvls_top_dungeon = []

# Obteniendo info miembros
for i in range(0,guild_len):
    # Obteniendo info general
    nombre = data['members'][i]['character']['name']
    nombres.append(nombre)
    print(nombre)
    nivel = data['members'][i]['character']['level']
    niveles.append(nivel)
    print(nivel)
    realm = data['members'][i]['character']['realm']['slug']
    print(realm)
    realms.append(realm)
    datos_personaje = data['members'][i]['character']['key']['href'] # Endpoint para info personaje
    # Obteniendo info especifica personaje
    response = requests.get(datos_personaje+f"&locale={idioma_datos}",headers=headers)
    # Por alguna razón hay un personaje que no tiene info! (jugador inactivo?)
    if response.status_code == 404:
        print(f'Error 404 para "{nombre}" indice "{i+1}", todos los datos especificos seran vacíos\n')
        with open('./error_logs/404.txt','a',encoding='utf-8') as f:
            f.write(f'[{time.ctime()}] Error 404 para "{nombre}" indice "{i+1}", todos los datos especificos seran vacíos, ¿Usuario inactivo?\n')
        ## Faccion
        faccion = ''
        facciones.append(faccion)
        ## Raza
        raza = ''
        razas.append(raza)
        ## Clase
        clase = ''
        clases.append(clase)
        ## Spec Activa
        spec_activa = ''
        specs_activas.append(spec_activa)
        ## Item lvl
        item_lvl = ''
        item_lvls.append(item_lvl)
        ## Mythic rating
        myth_rating = ''
        rating_miticas.append(myth_rating)
        ## Lvl mejor llave
        lvl_mejor_llave = ''
        mejores_llaves.append(lvl_mejor_llave)
        ## Datos mejor dungeon
        nombre_mejor_dung = ''
        nombre_mejores_llaves.append(nombre_mejor_dung)
        nivel_mejor_llave = ''
        lvls_top_dungeon.append(nivel_mejor_llave)
    else:
        data_personaje = response.json()
        # Almacenando datos
        ## Faccion
        faccion = data_personaje['faction']['name']
        print(faccion)
        facciones.append(faccion)
        ## Raza
        raza = data_personaje['race']['name']
        print(raza)
        razas.append(raza)
        ## Clase
        clase = data_personaje['character_class']['name']
        print(clase)
        clases.append(clase)
        ## Spec activa
        spec_activa = data_personaje['active_spec']['name']
        print(spec_activa)
        specs_activas.append(spec_activa)
        ## Item LVL
        item_lvl = data_personaje['equipped_item_level']
        print(item_lvl)
        item_lvls.append(item_lvl)
        # Endpoint informacion miticas
        datos_miticas = data_personaje['mythic_keystone_profile']['href']
        # Obteniendo datos miticas
        response = requests.get(datos_miticas+f"&locale={idioma_datos}",headers=headers)
        if response.status_code == 404:
            myth_rating = ''
            rating_miticas.append(myth_rating)
            lvl_mejor_llave = ''
            mejores_llaves.append(lvl_mejor_llave)
            ## Datos mejor dungeon
            nombre_mejor_dung = ''
            nombre_mejores_llaves.append(nombre_mejor_dung)
            nivel_mejor_llave = ''
            lvls_top_dungeon.append(nivel_mejor_llave)
        else:
            # Datos miticas json
            pj_miticas = response.json()
            # Rating
            try:
                myth_rating = pj_miticas['current_mythic_rating']['rating']
                rating_miticas.append(myth_rating)
            except:
                myth_rating = ''
                rating_miticas.append(myth_rating)
            # Obteniendo nivel llaves
            ## Lista nivel llaves
            # Mejor llave
            lista_lvl_llaves = []
            try:
                n_runs = len(pj_miticas['current_period']['best_runs']) # cantidad de runs
                for i in range(0,n_runs-1):
                    keyrun = pj_miticas['current_period']['best_runs'][i]['mythic_rating']['rating']
                    print(f'Llave {i+1} : {keyrun}')
                    lista_lvl_llaves.append(keyrun)
                if len(lista_lvl_llaves) >= 1:
                    lvl_mejor_llave = max(lista_lvl_llaves)
                    mejores_llaves.append(lvl_mejor_llave)
                else:
                    lvl_mejor_llave = ''
                    mejores_llaves.append(lvl_mejor_llave)
            except:
                lvl_mejor_llave = ''
                mejores_llaves.append(lvl_mejor_llave)
            print(f'Mejor lvl llave : {lvl_mejor_llave}')

            # Indice mejor llave
            try:
                indice_mejorllave = lista_lvl_llaves.index(max(lista_lvl_llaves))
            except Exception as error:
                indice_mejorllave = 0
            # Nombre mejor llave
            try:
                ## Datos mejor dungeon
                nombre_mejor_dung = pj_miticas["current_period"]["best_runs"][indice_mejorllave]["dungeon"]["name"]
                nombre_mejores_llaves.append(nombre_mejor_dung)
                nivel_mejor_llave = pj_miticas["current_period"]["best_runs"][indice_mejorllave]["keystone_level"]
                lvls_top_dungeon.append(nivel_mejor_llave)
                print(f'Nombre mejor dungeon : {nombre_mejor_dung}')
            except:
                ## Datos mejor dungeon
                nombre_mejor_dung = ''
                nombre_mejores_llaves.append(nombre_mejor_dung)
                nivel_mejor_llave = ''
                lvls_top_dungeon.append(nivel_mejor_llave)



# Creando DF

roster_db = pd.DataFrame(columns=['nombre',
                                  'nivel',
                                  'servidor',
                                  'faccion',
                                  'raza',
                                  'clase',
                                  'spec_activa',
                                  'item_lvl',
                                  'myth_rating',
                                  'mejor_rating',
                                  'mejor_dungeon',
                                  'mejor_key_lvl'])

# Asignando valores a columnas

roster_db['nombre'] = nombres
roster_db['nivel'] = niveles
roster_db['servidor'] = realms
roster_db['faccion'] = facciones
roster_db['raza'] = razas
roster_db['clase'] = clases
roster_db['spec_activa'] = specs_activas
roster_db['item_lvl'] = item_lvls
roster_db['myth_rating'] = rating_miticas
roster_db['mejor_rating'] = mejores_llaves
roster_db['mejor_dungeon'] = nombre_mejores_llaves
roster_db['mejor_key_lvl'] = lvls_top_dungeon

# Creando CSV

roster_db.to_csv("guild_roster_wow.csv",
                 index=False,
                 encoding="utf-8")



