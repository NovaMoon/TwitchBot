import json
import requests
import datetime
import pprint


def command_runner(msg, sender):
    data = 'data'
    user = msg[1]
    games = []
    runtimes = []
    runplaces = []
    runcats = []
    rungames = []
    i = 0
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
    if len(msg)<=3:
        if len(games) == 1:
            print('%s has run the following games: %s.' % (name, gamestr))
        else:
            print("%s has run the following games and %i others: %s."% (name, (len(games)-5), gamestr))
            print("/w %s The full list of games %s has run is: %s." %(sender, name, fullgamestr))
    else:
        for run in runs:
            run['game']['data']['names']['international'] = run['game']['data']['names']['international'].lower()
            if msg[2] in run['game']['data']['names']['international'].replace(" ", ""):
                time = run['run']['times']['primary_t']
                runtime = str(datetime.timedelta(seconds=time))
                runtimes.append(runtime)
                runplaces.append(run['place'])
                runcats.append(run['category']['data']['name'])
                rungames.append(run['game']['data']['names']['international'])
        if len(rungames)>1:
            print('%s has a run in %i categories of %s.' % (name, len(runcats), rungames[0]))
    pprint.pprint(rungames)
msg =  ['!runner', 'jumpyluff', '']
sender = 'litewarior'
command_runner(msg, sender)