# Librerias
import requests
import pandas as pd
from requests.auth import HTTPBasicAuth
import json

# Funcion para obtener el access token

def create_access_token(client_id, client_secret, region = 'us'):
    url = "https://oauth.battle.net/token"
    body = {"grant_type": 'client_credentials'}
    auth = HTTPBasicAuth(client_id, client_secret)

    response = requests.post(url, data=body, auth=auth)
    return response.json()


access_token = create_access_token("8d326e6f147f498f8c1d400284d9adda","DNKCsnqQEnaPWnVwnQ76cU7mg4k5UZSL")['access_token']

headers = {"Authorization" : f"Bearer {access_token}"}
url_wow = "https://us.api.blizzard.com/data/d3/season/9/leaderboard/rift-team-4?namespace=2-6-US"

response = requests.get(url_wow,headers=headers)

print(response.status_code)
data = response.json()
data_json = json.dumps(data,indent=4)

# Obteniendo cantidad de jugadores por equipo y cantidad de equipos
players_x_team= len(data['row'][0]['player'])
n_teams = len(data['row'])

print(players_x_team)
print(n_teams)

# Futuras listas para cread DF's
ranking = []
groups = []

# Obteniendo datos
for k in range(0,n_teams):
    ranking.append(k+1)
    group_raw = []
    for i in range(0,players_x_team):
        try:
            group_raw.append(data['row'][k]['player'][i]['data'][0]['string'])
        except KeyError:
            group_raw.append(data['row'][k]['player'][i]['data'][0]['number'])
        except IndexError:
            for i in range(0,players_x_team-1):
                try:
                    group_raw.append(data['row'][k]['player'][i]['data'][0]['string'])
                except KeyError:
                    group_raw.append(data['row'][k]['player'][i]['data'][0]['number'])
    groups.append(group_raw)

# Probando
for i in range(0,50):
    print(f"Rift Group Rank : {ranking[i]}")
    print("------------------")
    print(f"{groups[i]}")
    print("------------------")

# Creando el CSV

df = pd.DataFrame(columns=["rank","members"])

df["rank"] = ranking
df["members"] = groups

df.to_csv("s9_4man_ranking.csv",index=False)


