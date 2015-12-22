import json
import requests
import datetime
import pprint
from Pastebin import PastebinAPI

PASTEKEY = '4d150744923e05e1eb047ec0f613fe28'


def command_runner(msg, PASTEKEY):
    x = PastebinAPI()
    data = 'data'
    user = msg[1]
    games = []
    runtimes = []
    runplaces = []
    runcats = []
    rungames = []
    runstrlist = [['Game', 'Category', 'Place', 'Time']]
    i = 1
    runner = requests.get('http://www.speedrun.com/api/v1/users?name=%s' % user)
    rjs = json.loads(runner.text)
    try:
        rjs['data']
    except:
        print('No runner found with that name.')
        return(None)
    id = rjs[data][0]['id']
    name = rjs[data][0]['names']['international']
    pbs = requests.get('http://www.speedrun.com/api/v1/users/%s/personal-bests?embed=game,category' % id)
    pbjs = json.loads(pbs.text)
    runs = pbjs[data]
    for run in runs:
        gamename = run['game']['data']['names']['international']
        if gamename not in games:
            games.append(gamename)
    gamestr = ', '.join(games[:5])
    fullgamestr = ', '.join(games)
    for run in runs:
        run['game']['data']['names']['international'] = run['game']['data']['names']['international'].lower()
        time = run['run']['times']['primary_t']
        runtime = str(datetime.timedelta(seconds=time))
        runtimes.append(runtime)
        runplaces.append(str(run['place']))
        runcats.append(run['category']['data']['name'])
        rungames.append(run['game']['data']['names']['international'])
        i = i+1
    print(runstr)
msg =  ['!runner', 'stinkycheeseone890', '']
command_runner(msg, PASTEKEY)
