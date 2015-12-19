import json
import requests
import datetime
def command_wr(msg):
    game=msg[1]
    r=requests.get('http://www.speedrun.com/api/v1/games?name=kamilia3' % game)
    rjs=json.loads(r.text)
    try:
        rjs['data'][0]['names']['international']
    except:
        send_message(cfg.CHAN, 'No game found.')
        return None
    gamename=rjs['data'][0]['names']['international']
    category=rjs['data'][0]['links'][4]['uri']
    catlink=requests.get(category)
    cjs=json.loads(catlink.text)
    try:
        cjs['data'][0]['name']
    except:
        send_message(cfg.CHAN, 'No game found.')
        return(None)
    catname=cjs['data'][0]['name']
    records=cjs['data'][0]['links'][3]['uri']
    reclink=requests.get(records)
    recjs=json.loads(reclink.text)
    try:
        recjs['data'][0]['runs'][0]['run']
    except:
        send_message(cfg.CHAN, 'No runs found for %s.' gamename)
        return(None)
    wr=recjs['data'][0]['runs'][0]['run']
    time=wr['times']['primary_t']
    timename=str(datetime.timedelta(seconds=time))
    playerlink=wr['players'][0]['uri']
    player=requests.get(playerlink)
    pjs=json.loads(player.text)
    playername=pjs['data']['names']['international']
    send_message(cfg.CHAN, 'The record in %s %s is held by %s with %s' % (gamename, catname, playername, timename))