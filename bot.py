#!/usr/bin/python3.5
import cd
import cfg
import re
import requests
import socket
import sys
from threading import Timer
import os
import time
import datetime
import simplejson as json
from bs4 import UnicodeDammit

sys.dont_write_bytecode = True


# ---------------------------------- Start Functions ----------------------------------------------------



def send_pong(msg):
    con.send(bytes('PONG %s\r\n' % msg, 'UTF-8'))


def send_message(chan, msg):
    con.send(bytes('PRIVMSG %s :%s\r\n' % (chan, msg), 'UTF-8'))


def send_nick(nick):
    con.send(bytes('NICK %s\r\n' % nick, 'UTF-8'))


def send_pass(password):
    con.send(bytes('PASS %s\r\n' % password, 'UTF-8'))


def join_channel(chan):
    con.send(bytes('JOIN %s\r\n' % chan, 'UTF-8'))


def part_channel(chan):
    con.send(bytes('PART %s\r\n' % chan, 'UTF-8'))


# --------------------------------------------- End Functions ------------------------------------------------------


# --------------------------------------------- Start Helper Functions ---------------------------------------------
def get_sender(msg):
    result = ""
    for char in msg:
        if char == "!":
            break
        if char != ":":
            result += char
    return result


def get_message(msg):
    result = ""
    i = 3
    length = len(msg)
    while i < length:
        result += msg[i] + " "
        i += 1
    result = result.lstrip(':')
    return result


def parse_message(msg):
    if len(msg) >= 1:
        msg = msg.split(' ')
        options = {'!uptime': command_uuptime,
                   '!wr': command_wr}

        if msg[0] in options:
            if '!wr' in [msg[0]]:
                options[msg[0]](msg, sender)
            else:
                options[msg[0]]()


# --------------------------------------------- End Helper Functions -----------------------------------------------

# --------------------------------------------- Start Twitch API -----------------------------------------------


def get_chatters():
    try:
        global chatters
        global mods
        global plebs
        response = requests.get('https://tmi.twitch.tv/group/user/stinkycheeseone890/chatters')
        readable = response.text
        chatlist = json.loads(readable)
        chatters = chatlist['chatters']
        mods = chatters['moderators']
        plebs = chatters['viewers']
    except:
        print('Bad Gateway 502! Check again in 90sec')   # if you get alot of those, don't worry its twitch related and nothing you can do
    t = Timer(90.0, get_chatters)
    t.start()


get_chatters()


# --------------------------------------------- End Twitch API -----------------------------------------------

# --------------------------------------------- Start Command Functions --------------------------------------------


def command_wr(msg, sender):
    """queries speedrun.com api for game and category in game if specified, and returns data about world record run"""
    if sender in mods or (sender not in wrsenders and cd.cdwr == 0):
        if len(msg) >= 3:
            datename = 'unknown'
            cats = []
            catreq = 1
            catpos = 0
            account = 1
            try:  # checks if message has a category specified
                msg[3]
            except:
                catreq = 0
            game = msg[1]
            r = requests.get('http://www.speedrun.com/api/v1/games?name=%s' % game)
            rjs = json.loads(r.text)
            try:  # makes sure game exists
                rjs['data'][0]['names']['international']
            except:
                send_message(cfg.CHAN, 'No game found.')
                return None
            gamename = rjs['data'][0]['names']['international']
            category = rjs['data'][0]['links'][4]['uri']
            catlink = requests.get(category)
            cjs = json.loads(catlink.text)
            try:  # makes sure there are categories of the game
                cjs['data'][0]['name']
            except:
                send_message(cfg.CHAN, 'No categories found.')
                return None
            if catreq == 1:
                for cat in cjs['data']:
                    cats.append(cat['name'])
                    cats[-1] = str.lower(cats[-1])
                catname = ''
                if msg[2] in cats:
                    catname = msg[2]
                    catpos = cats.index(msg[2])
                else:
                    for cat in cats:
                        if msg[2] in cat:
                            while not catname:
                                catname = cat
                                catpos = cats.index(cat)
                    if not catname:
                        catname = cjs['data'][catpos]['name']
            else:
                catname = cjs['data'][catpos]['name']
            records = cjs['data'][catpos]['links'][3]['uri']
            reclink = requests.get(records)
            recjs = json.loads(reclink.text)
            try:  # makes sure there are runs for the category
                recjs['data'][0]['runs'][0]['run']
            except:
                send_message(cfg.CHAN, 'No runs found for %s, %s.' % (gamename, catname))
                return None
            wr = recjs['data'][0]['runs'][0]['run']
            try:
                datename = wr['date']
            except:
                print('No date found')
            time = wr['times']['primary_t']
            timename = str(datetime.timedelta(seconds=time))
            playerlink = wr['players'][0]['uri']
            player = requests.get(playerlink)
            pjs = json.loads(player.text)
            try:  # checks if player has an account
                pjs['data']['names']['international']
            except:
                account = 0
            if account == 1:
                playername = pjs['data']['names']['international']
            else:
                try:  # if player doesn't have a name errors out
                    pjs['data']['name']
                except:
                    send_message(cfg.CHAN, 'Error: Player doesn\'t exist.')
                    return None
                playername = pjs['data']['name']
            send_message(cfg.CHAN,
                         'The record in %s, %s was achieved by %s, on %s with %s'
                         % (gamename, catname, playername, datename, timename))
            wrsenders.append(sender)
            twr = Timer(180.0, wr_remove, [sender])
            twr.start()
            cd.cdwr = 1

            def testchange():
                cd.cdwr = 0

            t = Timer(30.0, testchange)
            t.start()
        else:
            send_message(cfg.CHAN, 'Specify a game.')


def wr_remove(sender):
    wrsenders.remove(sender)


def command_uuptime():
    if sender in mods:
        r = requests.get('https://decapi.me/twitch/uptime.php?channel=PasteYourChannelHere')
        send_message(cfg.CHAN, 'This channel has been live for: %s' % r.text)
    else:
        if cd.cduuptime == 0:
            r = requests.get('https://decapi.me/twitch/uptime.php?channel=PasteYourChannelHere')
            send_message(cfg.CHAN, 'This channel has been live for: %s' % r.text)
            cd.cduuptime = 1

        def cooldown():
            cd.cduuptime = 0

        t = Timer(30.0, cooldown)
        t.start()

# --------------------------------------------End Command Functions--------------------------------------------

# ---------------------------------------Start Running Code----------------------------------------------------

con = socket.socket()
con.connect((cfg.HOST, cfg.PORT))

send_pass(cfg.PASS)
send_nick(cfg.NICK)
join_channel(cfg.CHAN)

data = ""

wrsenders = ['']
logpath = '/home/nova/twitchbot/chat/stinkycheeseone890/' # linux path for your logfile
if not os.path.isfile(logpath + "log.txt"):
    print("Creating log file for" + cfg.CHAN)
    if not os.path.isdir(logpath): os.makedirs(logpath)


def formatdate():
    while True:
        now = datetime.date.today()
        return "[" + " ".join([now.strftime("%A")[0:3], now.strftime("%B")[0:3], now.strftime("%d"),
                               datetime.datetime.now().strftime("%H:%M:%S"), time.tzname[0], now.strftime("%Y")]) + "]"


now = formatdate()

while True:
    try:
        data = data + con.recv(1024).decode('UTF-8')
        data_split = re.split(r"[\r\n]+", data)
        data = data_split.pop()
        for line in data_split:
            line = str.rstrip(line)
            line = str.split(line)

            if len(line) >= 1:
                if line[0] == 'PING':
                    send_pong(line[1])

                if line[1] == 'PRIVMSG':
                    sender = get_sender(line[0])
                    message = get_message(line)
                    parse_message(message)
                    for word in cfg.PATT:
                        if word in message:
                            send_message(cfg.CHAN, '/ban  %s ' % sender)
                            send_message(cfg.CHAN, 'banned for being a shithead 4Head')

                    print(sender + ": " + message)

                    with open(logpath + 'log.txt', 'a+') as f:
                        f.write('%s %s: %s\n"' % (now, sender, UnicodeDammit(message).unicode_markup.encode(
                                'utf8')))  # encode characters like ( •ᴗ•) so it wont crash the bot





    except socket.error:
        print("Socket died")

    except socket.timeout:
        print("Socket timeout")
