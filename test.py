import json
import requests
import datetime
import pprint
def command_wr(msg):
    cats=[]
    catreq=1
    catpos=0
    try:
        msg[3]
    except:
        catreq=0
    game=msg[1]
    r=requests.get('http://www.speedrun.com/api/v1/games?name=%s' % game)
    rjs=json.loads(r.text)
    try:
        rjs['data'][0]['names']['international']
    except:
        print('No game found.')
        return None
    gamename=rjs['data'][0]['names']['international']
    category=rjs['data'][0]['links'][4]['uri']
    catlink=requests.get(category)
    cjs=json.loads(catlink.text)
    try:
        cjs['data'][0]['name']
    except:
        print('No game found.')
        return(None)
    if (catreq==1):
        for cat in cjs['data']:
            cats.append(cat['name'])
            cats[-1]=str.lower(cats[-1])
        catname=''
        for cat in cats:
            if msg[2] in cats:
                catname=msg[2]
                catpos=cats.index(msg[2])
            else:
                if msg[2] in cat:
                    while not catname:
                        catname=cat
                        catpos=cats.index(cat)
        if not catname:
            catname=cjs['data'][0]['name']
    else:
        catname=cjs['data'][0]['name']
    records=cjs['data'][catpos]['links'][3]['uri']
    reclink=requests.get(records)
    recjs=json.loads(reclink.text)
    try:
        recjs['data'][0]['runs'][0]['run']
    except:
        print('No runs found for %s, %s.' % (gamename, catname))
        return(None)
    wr=recjs['data'][0]['runs'][0]['run']
    time=wr['times']['primary_t']
    timename=str(datetime.timedelta(seconds=time))
    playerlink=wr['players'][0]['uri']
    player=requests.get(playerlink)
    pjs=json.loads(player.text)
    playername=pjs['data']['names']['international']
    #pprint.pprint(cjs['data'][catpos])
    print('The record in %s %s is held by %s with %s' % (gamename, catname, playername, timename))
msg=['!wr', 'kamilia3']
command_wr(msg)