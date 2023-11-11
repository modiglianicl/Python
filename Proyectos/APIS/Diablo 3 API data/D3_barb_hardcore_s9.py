import requests
import pandas as pd
from requests.auth import HTTPBasicAuth

# Funcion para obtener el access token

def create_access_token(client_id, client_secret, region = 'us'):
    url = "https://oauth.battle.net/token"
    body = {"grant_type": 'client_credentials'}
    auth = HTTPBasicAuth(client_id, client_secret)

    response = requests.post(url, data=body, auth=auth)
    return response.json()


access_token = create_access_token("8d326e6f147f498f8c1d400284d9adda","DNKCsnqQEnaPWnVwnQ76cU7mg4k5UZSL")['access_token']
print(create_access_token("8d326e6f147f498f8c1d400284d9adda","DNKCsnqQEnaPWnVwnQ76cU7mg4k5UZSL"))

# Parametros para el requests

headers = {"Authorization" : f"Bearer {access_token}"}
url_wow = "https://us.api.blizzard.com/data/d3/season/9/leaderboard/rift-hardcore-barbarian?namespace=2-6-US"

response = requests.get(url_wow,headers=headers)

print(response.status_code)
data = response.json()


# Obteniendo leaderboard season 9 barbaros hardcore

player = []
clase_player = []
rank_player = []

for i in range(0,len(data['row'])):
    # Hacemos try con string sino con number, ya que hay battletags "anonimos"
    try:
        nombre_player = data['row'][i]['player'][0]['data'][0]['string']
        player.append(nombre_player)
    except:
        nombre_player = data['row'][i]['player'][0]['data'][0]['number']
        player.append(nombre_player)
    clase_player_raw =  data['row'][i]['player'][0]['data'][2]['string']
    clase_player.append(clase_player_raw)
    rank_player_raw = data['row'][i]['data'][0]['number']
    rank_player.append(rank_player_raw)
    print(f"Rank {rank_player} : {nombre_player}. Clase : {clase_player}")

# Creamos el DF

df = pd.DataFrame(columns=["rank","player","clase"])

df['rank'] = rank_player
df['player'] = player
df['clase'] = clase_player

df.to_csv("s9_barb_hc.csv",index=False)