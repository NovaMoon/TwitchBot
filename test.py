import json
import requests
import pprint
r=requests.get('http://www.speedrun.com/api/v1/games?name=k3')
rjs=json.loads(r.text)
title=rjs['data']
pprint.pprint(rjs)
