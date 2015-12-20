import json
import requests
import datetime
import pprint


def command_runner(msg):
    data = 'data'
    user = msg[1]
    games = []
    runtimes = []
    runplaces = []
    runcats = []
    rungames = []

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
    gamestr = ', '.join(games)
    if len(msg)<=3:
        print('%s has run the following games: %s' % (name, gamestr))
    else:
        for run in runs:
            if msg[2] in run['game']['data']['names']['international']:
                time = run['run']['times']['primary_t']
                runtime = str(datetime.timedelta(seconds=time))
                runtimes.append(runtime)
                runplaces.append(run['run']['place'])
                runcats.append(run['category']['data']['name'])
                rungames.append(run['game']['data']['names']['international'])
    print(runtimes)
msg=  ['!runner', 'stinkycheeseone890','boshy', '']
command_runner(msg)